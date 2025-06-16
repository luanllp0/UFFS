package backend.backend.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDate;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Emprestimo {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    Long id;

    @ManyToOne
    Livro livro;

    @ManyToOne
    Usuario usuario; 

    LocalDate dataEmprestimo;
    LocalDate dataDevolucaoPrevista;
    
    @Override
    public String toString() {
    return "Livro: '" + this.getLivro().getTitulo() + "' - Usuário: '" + this.getUsuario().getNome() + "'";
}
}