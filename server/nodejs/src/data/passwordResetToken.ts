import { prisma } from "../index";

export async function getPasswordResetTokenByEmail(email: string) {
  const passwordResetToken = await prisma.passwordResetToken.findFirst({
    where: {
      email,
    },
  });
  return passwordResetToken;
}

export async function getPasswordResetTokenByToken(token: string) {
  const passwordResetToken = await prisma.passwordResetToken.findUnique({
    where: {
      token,
    },
  });
  return passwordResetToken;
}
