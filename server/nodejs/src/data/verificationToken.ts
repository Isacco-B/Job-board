import { prisma } from "../index";

export async function getVerificationTokenByEmail(email: string) {
  const verificationToken = await prisma.verificationToken.findFirst({
    where: {
      email,
    },
  });

  return verificationToken;
}
export async function getVerificationTokenByToken(token: string) {
  const verificationToken = await prisma.verificationToken.findUnique({
    where: {
      token,
    },
  });

  return verificationToken;
}
