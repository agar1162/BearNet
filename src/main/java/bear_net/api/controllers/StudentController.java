package bear_net.api.controllers;

import bear_net.api.models.Student;
import bear_net.api.models.dto.StudentDTO;
import bear_net.api.services.StudentService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/students")
public class StudentController {

    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @PostMapping
    public Student createStudent(@RequestBody Student student) {
        return studentService.createStudent(student);
    }

    @GetMapping
    public List<StudentDTO> getAllStudents() {
        return studentService.getAllStudents();
    }

    @PostMapping("/{studentId}/courses/{courseId}")
    public StudentDTO enrollStudentInCourse(@PathVariable Long studentId,
                                            @PathVariable Long courseId) {
        return studentService.enrollStudentInCourse(studentId, courseId);
    }
}