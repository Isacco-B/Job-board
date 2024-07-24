import { prisma } from "../index";

export async function getAccountByEmail(userId: string) {
  const profile = await prisma.profile.findUnique({
    where: {
      userId,
    },
  });

  return profile;
}
