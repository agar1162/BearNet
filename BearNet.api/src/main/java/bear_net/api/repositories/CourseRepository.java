package bear_net.api.repositories;

import bear_net.api.models.Course;
import org.springframework.data.repository.ListCrudRepository;

public interface CourseRepository extends ListCrudRepository<Course,Long>{
}
