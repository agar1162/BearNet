package bear_net.api.mappers;

import bear_net.api.models.Course;
import bear_net.api.models.Student;
import bear_net.api.models.dto.CourseDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Named;
import java.util.List;

@Mapper(componentModel = "spring")
public interface CourseDTOMapper {

    @Mapping(target = "studentNames", source = "students", qualifiedByName = "studentsToNames")
    CourseDTO toDTO(Course course);

    List<CourseDTO> toDTOList(List<Course> courses);

    @Named("studentsToNames")
    default List<String> studentsToNames(List<Student> students) {
        if (students == null) return null;
        return students.stream()
                .map(Student::getName)
                .toList();
    }
}
