import type { CourseDTO } from "./course";

export type StudentDTO = {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
  courses: CourseDTO[];
  username: string;
};