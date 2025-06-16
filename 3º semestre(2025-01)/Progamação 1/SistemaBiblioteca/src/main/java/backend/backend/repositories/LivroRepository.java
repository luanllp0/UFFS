package backend.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import backend.backend.entities.Livro;

public interface LivroRepository extends JpaRepository<Livro, Long> {
    
}
