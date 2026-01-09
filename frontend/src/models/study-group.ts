import type { StudyGroupMemberDTO } from "./study-group-member";

export type StudyGroupDTO = {
  id: number;
  location: string;
  courseTitle: string;
  meetingTime: string;
  meetingDay?: string;
  members: StudyGroupMemberDTO[];
};