package backend.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import backend.backend.entities.Emprestimo;

public interface EmprestimoRepository extends JpaRepository<Emprestimo, Long> {
    
}
