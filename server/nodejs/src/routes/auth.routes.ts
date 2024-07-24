import express, { Router } from "express";
import {
  newPassword,
  newVerification,
  register,
} from "../controllers/auth.controller";

const router: Router = express.Router();

router.post("/sign-up", register);
router.post("/new-password/:token", newPassword);
router.post("/new-verification/:token", newVerification);

export default router;
