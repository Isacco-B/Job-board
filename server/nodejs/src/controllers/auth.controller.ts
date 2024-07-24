import { NextFunction, Request, Response } from "express";
import { prisma } from "../index";
import { errorHandler } from "../middleware/errorHandler";
import bcrypt from "bcryptjs";
import jwt, { JwtPayload } from "jsonwebtoken";
import {
  LoginSchema,
  NewPasswordSchema,
  RegisterSchema,
  ResetSchema,
} from "../schemas";
import {
  generatePasswordResetToken,
  generateVerificationToken,
} from "../utils/tokens";
import { sendVerificationEmail } from "../utils/emails/sendVerificationEmail";
import { getUserByEmail, getUserById } from "../data/user";
import { ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET } from "../secrets";
import { getVerificationTokenByToken } from "../data/verificationToken";
import { sendPasswordResetEmail } from "../utils/emails/sendPasswordResetEmail";
import { getPasswordResetTokenByToken } from "../data/passwordResetToken";

const REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;

export async function register(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const validatedFields = RegisterSchema.safeParse(req.body);

  if (!validatedFields.success) {
    return next(errorHandler(400, "Invalid fields!"));
  }

  const { name, email, password, confirmPassword } = validatedFields.data;

  try {
    if (password !== confirmPassword) {
      return next(errorHandler(400, "Passwords do not match!"));
    }

    if (!REGEX.test(password)) {
      return next(
        errorHandler(
          400,
          "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        )
      );
    }

    const existingUser = await getUserByEmail(email);

    if (existingUser) return next(errorHandler(400, "User already exists"));

    const hashPassword = await bcrypt.hash(password, 10);

    await prisma.user.create({ data: { name, email, password: hashPassword } });

    const newVerificationToken = await generateVerificationToken(email);
    await sendVerificationEmail(email, newVerificationToken.token);

    return res.status(201).json({ message: "Confirmation email sent!" });
  } catch (error) {
    next(error);
  }
}

export async function login(req: Request, res: Response, next: NextFunction) {
  const validatedFields = LoginSchema.safeParse(req.body);

  if (!validatedFields.success) {
    return next(errorHandler(400, "Invalid fields!"));
  }

  const { email, password } = validatedFields.data;

  try {
    const existingUser = await getUserByEmail(email);
    if (!existingUser || !existingUser.email || !existingUser.password) {
      return next(errorHandler(400, "User not found"));
    }

    if (!existingUser.emailVerified) {
      const verificationToken = await generateVerificationToken(email);
      await sendVerificationEmail(
        verificationToken.email,
        verificationToken.token
      );
      return res.status(201).json({ message: "Confirmation email sent!" });
    }

    const validPassword = await bcrypt.compare(password, existingUser.password);
    if (!validPassword) {
      return next(errorHandler(400, "Invalid credentials"));
    }

    const accessToken = jwt.sign(
      {
        id: existingUser.id,
        email: existingUser.email,
      },
      ACCESS_TOKEN_SECRET,
      { expiresIn: "15m" }
    );

    const refreshToken = jwt.sign(
      { id: existingUser.id },
      REFRESH_TOKEN_SECRET,
      { expiresIn: "7d" }
    );

    res.cookie("jwt", refreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: "none",
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    return res.status(200).json({ accessToken });
  } catch (error) {
    next(error);
  }
}

export async function logout(req: Request, res: Response, next: NextFunction) {
  const cookie = req.cookies["jwt"];
  if (!cookie) {
    return next(errorHandler(404, "No cookie found"));
  }
  res.clearCookie("jwt", { httpOnly: true, sameSite: "none", secure: true });
  return res.status(200).json({ message: "Logout successful" });
}

export async function refresh(req: Request, res: Response, next: NextFunction) {
  const refreshToken = req.cookies["jwt"];
  if (!refreshToken) {
    return next(errorHandler(401, "Unauthorized!"));
  }
  try {
    jwt.verify(
      refreshToken,
      REFRESH_TOKEN_SECRET,
      async (err: jwt.VerifyErrors, decoded: JwtPayload) => {
        if (err) return next(errorHandler(403, "Forbidden!"));
        const user = await getUserById(decoded.id);
        if (!user) return next(errorHandler(404, "User not found!"));
        const accessToken = jwt.sign(
          {
            id: user.id,
            email: user.email,
          },
          ACCESS_TOKEN_SECRET,
          { expiresIn: "15m" }
        );
        return res.status(200).json({ accessToken });
      }
    );
  } catch (error) {
    next(error);
  }
}

export async function reset(req: Request, res: Response, next: NextFunction) {
  const validatedFields = ResetSchema.safeParse(req.body);
  if (!validatedFields.success) {
    return next(errorHandler(400, "Invalid fields!"));
  }
  const { email } = validatedFields.data;

  try {
    const existingUser = await getUserByEmail(email);
    if (!existingUser) return next(errorHandler(404, "Email not found!"));
    const passwordResetToken = await generatePasswordResetToken(email);
    await sendPasswordResetEmail(
      passwordResetToken.email,
      passwordResetToken.token
    );
    return res.status(200).json({ message: "Reset email sent!" });
  } catch (error) {
    next(error);
  }
}

export async function newPassword(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const { token } = req.params;
  if (!token) {
    return next(errorHandler(400, "Missing token!"));
  }
  const validatedFields = NewPasswordSchema.safeParse(req.body);
  if (!validatedFields.success) {
    return next(errorHandler(400, "Invalid fields!"));
  }
  const { password, confirmPassword } = validatedFields.data;

  try {
    if (password !== confirmPassword) {
      return next(errorHandler(400, "Passwords do not match!"));
    }

    if (!REGEX.test(password)) {
      return next(
        errorHandler(
          400,
          "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        )
      );
    }

    const existingToken = await getPasswordResetTokenByToken(token);
    if (!existingToken) return next(errorHandler(400, "Invalid token!"));

    const hasExpired = new Date(existingToken.expires) < new Date();
    if (hasExpired) {
      await prisma.passwordResetToken.delete({
        where: {
          id: existingToken.id,
        },
      });
      return next(errorHandler(400, "Token has expired!"));
    }

    const existingUser = await getUserByEmail(existingToken.email);
    if (!existingToken) return next(errorHandler(404, "User not found!"));

    const hashedPassword = await bcrypt.hash(password, 10);
    await prisma.user.update({
      where: {
        id: existingUser.id,
      },
      data: {
        password: hashedPassword,
      },
    });
    await prisma.passwordResetToken.delete({
      where: {
        id: existingToken.id,
      },
    });
    return res.status(200).json({ message: "Password reset successful!" });
  } catch (error) {
    next(error);
  }
}

export async function newVerification(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const { token } = req.params;

  if (!token) {
    return next(errorHandler(400, "Missing token!"));
  }

  try {
    const existingToken = await getVerificationTokenByToken(token);
    if (!existingToken) return next(errorHandler(400, "Invalid token!"));

    const hasExpired = new Date(existingToken.expires) < new Date();

    if (hasExpired) {
      await prisma.verificationToken.delete({
        where: {
          id: existingToken.id,
        },
      });
      return next(errorHandler(400, "Token has expired!"));
    }

    const existingUser = await getUserByEmail(existingToken.email);
    if (!existingUser) return next(errorHandler(404, "Email does not exist!"));

    await prisma.user.update({
      where: {
        id: existingUser.id,
      },
      data: {
        emailVerified: new Date(),
        email: existingToken.email,
      },
    });

    await prisma.verificationToken.delete({
      where: {
        id: existingToken.id,
      },
    });

    return res.status(200).json({ message: "Email verified!" });
  } catch (error) {
    next(error);
  }
}
