package bear_net.api.services;

import bear_net.api.mappers.CourseDTOMapper;
import bear_net.api.models.Course;
import bear_net.api.models.dto.CourseDTO;
import bear_net.api.repositories.CourseRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CourseService {

    private final CourseRepository courseRepository;
    private final CourseDTOMapper courseDTOMapper;

    public CourseService(CourseRepository courseRepository, CourseDTOMapper courseDTOMapper) {
        this.courseRepository = courseRepository;
        this.courseDTOMapper = courseDTOMapper;
    }

    public Course createCourse(Course course) {
        return courseRepository.save(course);
    }

    public List<CourseDTO> getAllCourses() {
        return courseRepository.findAll().stream()
                .map(courseDTOMapper::toDTO)
                .toList();
    }
}
