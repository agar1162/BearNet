package bear_net.api.repositories;


import bear_net.api.models.Student;
import org.springframework.data.repository.ListCrudRepository;

public interface StudentRepository extends ListCrudRepository<Student, Long> {
}
