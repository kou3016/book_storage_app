package com.example.demo.book;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface BookRepository extends JpaRepository<Book, Integer> {
    List<Book> findByTitleStartingWith(String title);
    List<Book> findByAuthorStartingWith(String author);
    List<Book> findByPublisherStartingWith(String publisher);
    List<Book> findByStatus(String status);
}