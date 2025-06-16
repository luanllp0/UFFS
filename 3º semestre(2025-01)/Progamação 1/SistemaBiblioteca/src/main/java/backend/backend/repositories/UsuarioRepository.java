package backend.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import backend.backend.entities.Usuario;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    
}
