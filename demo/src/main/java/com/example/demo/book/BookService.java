package com.example.demo.book;

import org.springframework.stereotype.Service;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;
import java.util.List;
import org.springframework.transaction.annotation.Transactional;
import java.util.Optional;

@Service
public class BookService {
    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    // 本データの登録
    public Book create(Book book) {
        return bookRepository.save(book);
    }

    // 本データの削除
    public void deleteById(Integer id) {
        if (!bookRepository.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found: " + id);
        }
        bookRepository.deleteById(id);
    }

    // 本データの更新
    public Book update(Integer id, Book req) {
    Book book = bookRepository.findById(id)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found"));

        book.setTitle(req.getTitle());
        book.setAuthor(req.getAuthor());
        book.setVolumes(req.getVolumes());
        book.setPublisher(req.getPublisher());
        book.setIsbn(req.getIsbn());
        book.setGenre(req.getGenre());
        book.setStatus(req.getStatus());

        return bookRepository.save(book);
    }

    // 一覧取得
    @Transactional
    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    // 詳細取得
    @Transactional
    public Optional<Book> getById(Integer id) {
        return bookRepository.findById(id);
    }

    // 検索機能
    public List<Book> search(String type, String keyword) {
        if(keyword == null || keyword.isBlank()) {
            return bookRepository.findAll();
        }

        return switch (type) {
            case "id" -> {
                try {
                    Integer id = Integer.valueOf(keyword);
                    yield bookRepository.findById(id).map(List::of).orElse(List.of());
                } catch (NumberFormatException e) {
                    yield List.of();
                } 
            }
            case "title" -> bookRepository.findByTitleStartingWith(keyword);
            case "author" -> bookRepository.findByAuthorStartingWith(keyword);
            default -> List.of();
        };
    }

}
