import { useState } from "react";
import { Link } from "react-router-dom";
import type { StudyGroupDTO } from "../models/study-group";
import type { StudentDTO } from "../models/student";

/* ======================
   MAIN PAGE
====================== */

type Props = {
  groupData: StudyGroupDTO[];
  studentData: StudentDTO;
};

export default function Home() {
  const [activeView, setActiveView] = useState<
    "default" | "find" | "create"
  >("default");

  const [error, setError] = useState<string | null>(null);
  const [studyGroups, setStudyGroups] =
    useState<StudyGroupDTO[]>();

  const student = null;

  async function handleCreateGroup(formData: FormData) {
    try {
      const res = await fetch("http://localhost:8000/study-groups", {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to create group");
      }

      const newGroup = await res.json();
      setStudyGroups((prev) => [...prev, newGroup]);
      setActiveView("default");
      setError(null);
    } catch (err) {
      setError("Could not create study group");
    }
  }

  return (
    <main className="w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="mx-auto max-w-screen-2xl px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-start">

          {/* MENU */}
          <aside className="bg-white rounded-3xl shadow-xl p-4 md:col-span-1 h-fit">
            <h2 className="text-2xl mb-4">Menu</h2>
            <div className="space-y-3">
              <MenuCardButton
                label="My Study Groups"
                active={activeView === "default"}
                onClick={() => setActiveView("default")}
              />
              <MenuCardButton
                label="Find Study Group"
                active={activeView === "find"}
                onClick={() => setActiveView("find")}
              />
              <MenuCardButton
                label="Create Study Group"
                active={activeView === "create"}
                onClick={() => setActiveView("create")}
              />
            </div>
          </aside>

          {/* MAIN CONTENT */}
          <section className="bg-white rounded-3xl shadow-xl p-4 md:col-span-3 min-h-[40vh]">

            {activeView === "default" && (
              <>
                <h2 className="text-2xl mb-4">My Study Groups</h2>

                {studyGroups.length === 0 ? (
                  <p className="text-gray-500">
                    You are not in any study groups yet.
                  </p>
                ) : (
                  <div className="grid gap-4">
                    {studyGroups.map((group) => (
                      <StudyGroupCard key={group.id} group={group} />
                    ))}
                  </div>
                )}
              </>
            )}

            {activeView === "create" && (
              <>
                <h2 className="text-2xl mb-4">Create Study Group</h2>

                {error && (
                  <p className="text-sm text-red-600 mb-3">{error}</p>
                )}

                <form
                  onSubmit={async (e) => {
                    e.preventDefault();
                    await handleCreateGroup(
                      new FormData(e.currentTarget)
                    );
                  }}
                >
                  <FormInput
                    label="Course Title"
                    name="courseTitle"
                    placeholder="EECS151, CS70, MATH1A"
                  />

                  <FormInput
                    label="Location"
                    name="location"
                    placeholder="Cory 555, Zoom..."
                  />

                  <FormInput
                    label="Meeting Time"
                    name="meetingTime"
                    type="time"
                  />

                  <button
                    type="submit"
                    className="mt-6 bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition"
                  >
                    Create Group
                  </button>
                </form>
              </>
            )}
          </section>

          {/* PROFILE */}
          <aside className="bg-white rounded-3xl shadow-xl p-5 md:col-span-1 h-fit">
            <h2 className="text-2xl font-semibold mb-5">About Me</h2>

            <div className="flex items-center gap-4 mb-5">
              <InitialAvatar name={student.firstname} size={72} />
              <div className="min-w-0">
                <p className="font-semibold text-lg truncate">
                  {student.firstname} {student.lastname[0]}.
                </p>
                <p className="text-sm text-gray-600 truncate">
                  @{student.username}
                </p>
              </div>
            </div>

            <div className="border-t border-gray-100 my-4" />

            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Major</span>
                <span className="font-medium">Computer Science</span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-500">Year</span>
                <span className="font-medium">Sophomore</span>
              </div>

              <div className="flex justify-between items-start gap-2">
                <span className="text-gray-500">Courses</span>
                <ul className="flex flex-wrap gap-2 justify-end">
                  {student.courses.map((course) => (
                    <li
                      key={course.id}
                      className="h-8 px-3 rounded-full bg-[#0A84FF] text-white text-sm flex items-center"
                    >
                      {course.title}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <button className="mt-6 w-full bg-gray-100 hover:bg-gray-200 text-sm font-medium py-2 rounded-lg transition">
              Edit Profile
            </button>
          </aside>
        </div>
      </div>
    </main>
  );
}

/* ======================
   COMPONENTS
====================== */

function StudyGroupCard({ group }: { group: StudyGroupDTO }) {
  return (
    <div className="rounded-xl bg-[#EFF6FF] border-l-4 border-[#002473] hover:bg-[#DBEAFE] p-4 shadow-sm hover:shadow-md transition">
      <p className="text-sm text-gray-600">📍 {group.location}</p>
      <p className="text-sm text-gray-600">🕒 {group.meetingTime}</p>

      <div className="flex items-center gap-2 mt-3">
        {group.members.slice(0, 5).map((member) => (
          <div key={member.id} className="relative group">
            <InitialAvatar name={member.name} size={32} />
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 rounded-md bg-gray-900 px-2 py-1 text-xs text-white opacity-0 group-hover:opacity-100 transition">
              {member.name}
            </div>
          </div>
        ))}

        {group.members.length > 5 && (
          <span className="text-xs text-gray-500">
            +{group.members.length - 5}
          </span>
        )}
      </div>

      <Link
        to={`/study-group/${group.id}`}
        className="inline-block mt-3 text-sm text-indigo-600 hover:underline"
      >
        View Group →
      </Link>
    </div>
  );
}

function MenuCardButton({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl transition shadow-sm hover:shadow-md text-lg border-l-4 ${
        active
          ? "bg-[#FEF3C7] border-[#F59E0B]"
          : "bg-[#FFFBEB] border-transparent hover:border-[#F59E0B]"
      }`}
    >
      <span className="font-medium text-gray-800">{label}</span>
    </button>
  );
}

function FormInput({
  label,
  name,
  type = "text",
  placeholder,
}: {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
}) {
  return (
    <>
      <label className="block text-sm font-medium text-gray-700 mb-1 mt-4">
        {label}
      </label>
      <input
        name={name}
        type={type}
        placeholder={placeholder}
        required
        className="md:w-[50%] w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none transition"
      />
    </>
  );
}

function InitialAvatar({
  name,
  size = 48,
}: {
  name?: string;
  size?: number;
}) {
  const initial = name?.trim()?.[0]?.toUpperCase() ?? "?";
  const colorClass = colorFromName(name);

  return (
    <div
      className={`flex items-center justify-center rounded-full font-semibold ${colorClass}`}
      style={{ width: size, height: size }}
    >
      <span className="leading-none text-lg">{initial}</span>
    </div>
  );
}

/* ======================
   UTILS
====================== */

const AVATAR_COLORS = [
  "bg-red-200 text-red-800",
  "bg-orange-200 text-orange-800",
  "bg-amber-200 text-amber-800",
  "bg-yellow-200 text-yellow-800",
  "bg-lime-200 text-lime-800",
  "bg-green-200 text-green-800",
  "bg-emerald-200 text-emerald-800",
  "bg-teal-200 text-teal-800",
  "bg-cyan-200 text-cyan-800",
  "bg-sky-200 text-sky-800",
  "bg-blue-200 text-blue-800",
  "bg-indigo-200 text-indigo-800",
  "bg-violet-200 text-violet-800",
  "bg-purple-200 text-purple-800",
  "bg-fuchsia-200 text-fuchsia-800",
  "bg-pink-200 text-pink-800",
];

function colorFromName(name?: string) {
  if (!name) return "bg-gray-200 text-gray-700";
  const charCode = name.trim().toUpperCase().charCodeAt(0);
  return AVATAR_COLORS[charCode % AVATAR_COLORS.length];
}
