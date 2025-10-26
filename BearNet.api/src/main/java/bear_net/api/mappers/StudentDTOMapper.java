package bear_net.api.mappers;

import bear_net.api.models.Course;
import bear_net.api.models.Student;
import bear_net.api.models.dto.StudentDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Named;

import java.util.List;
import java.util.stream.Collectors;

@Mapper(componentModel = "spring")
public interface StudentDTOMapper {

    @Mapping(target = "courses", source = "courses", qualifiedByName = "coursesToTitles")
    StudentDTO toDTO(Student student);

    List<StudentDTO> toDTOList(List<Student> students);

    @Named("coursesToTitles")
    default List<String> coursesToTitles(List<Course> courses) {
        if (courses == null) {
            return null;
        }
        return courses.stream()
                .map(Course::getTitle)
                .collect(Collectors.toList());
    }
}