package bear_net.api.services;

import bear_net.api.mappers.StudentDTOMapper;
import bear_net.api.models.Course;
import bear_net.api.models.Student;
import bear_net.api.models.dto.StudentDTO;
import bear_net.api.repositories.CourseRepository;
import bear_net.api.repositories.StudentRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StudentService {

    private final StudentRepository studentRepository;
    private final CourseRepository courseRepository;
    private final StudentDTOMapper studentDTOMapper;

    public StudentService(StudentRepository studentRepository,
                          CourseRepository courseRepository,
                          StudentDTOMapper studentDTOMapper) {
        this.studentRepository = studentRepository;
        this.courseRepository = courseRepository;
        this.studentDTOMapper = studentDTOMapper;
    }

    public Student createStudent(Student student) {
        return studentRepository.save(student);
    }

    public List<StudentDTO> getAllStudents() {
        List<Student> students = studentRepository.findAll();
        return studentDTOMapper.toDTOList(students);  // Fixed: use toDTOList() method
    }

    public StudentDTO enrollStudentInCourse(Long studentId, Long courseId) {
        Student student = studentRepository.findById(studentId)
                .orElseThrow(() -> new RuntimeException("Student not found"));
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new RuntimeException("Course not found"));

        student.getCourses().add(course);
        Student savedStudent = studentRepository.save(student);

        return studentDTOMapper.toDTO(savedStudent);  // Fixed: use toDTO() method
    }
}