import express, { Express, NextFunction, Request, Response } from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import compression from "compression";
import corsOptions from "./config/corsOptions";
import path from "path";
import { PrismaClient } from "@prisma/client";
import { NODE_ENV, PORT } from "./secrets";
import { HttpException } from "./exceptions";

import authRoutes from "./routes/auth.routes";

// const __dirname = import.meta.dirname;

export const prisma = new PrismaClient();

function startServer() {
  const app: Express = express();

  // Middleware
  app.use(cors(corsOptions));
  app.use(compression());
  app.use(cookieParser());
  app.use(express.json());

  // Static Files
  // app.use(express.static(path.join(__dirname, "media")));

  // Routes
  app.use("/api/auth", authRoutes);
  app.get("/", (req: Request, res: Response) => {
    res.send("Job Board API");
  });

  // 404
  app.all("*", (req: Request, res: Response) => {
    res.status(404);
    if (req.accepts("json")) {
      res.json({
        message: "404 Not Found",
      });
    } else {
      res.type("txt").send("404 Not Found");
    }
  });

  // Error handler
  app.use(
    (err: HttpException, req: Request, res: Response, next: NextFunction) => {
      const statusCode = err.statusCode || 500;
      const message = err.message || "Internal Server Error";
      res
        .status(statusCode)
        .json({ success: false, statusCode, message, isError: true });
    }
  );

  app.listen(PORT, () =>
    console.log(`Listening on ${NODE_ENV === "production" ? "https://demo7.isaccobertoli.com" : `http://localhost:${PORT}`}`)
  );
}

console.log("Connecting to database...");
prisma
  .$connect()
  .then(() => {
    console.log("Connected to database");
    startServer();
  })
  .catch((e) => {
    console.log("Failed to connect to database");
    console.log(e);
  });
