package bear_net.api.models.dto;

import java.util.List;

public class CourseDTO {
    private Long id;
    private String title;
    private List<String> studentNames;

    public CourseDTO(Long id, String title, List<String> studentNames) {
        this.id = id;
        this.title = title;
        this.studentNames = studentNames;
    }

    public Long getId() { return id; }
    public String getTitle() { return title; }
    public List<String> getStudentNames() { return studentNames; }
}
