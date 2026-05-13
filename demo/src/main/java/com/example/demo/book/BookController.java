package com.example.demo.book;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/books")
public class BookController {
    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    // 本データの登録
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Book create(@RequestBody Book book) {
        return bookService.create(book);
    }

    // 本データの削除
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Integer id) {
        bookService.deleteById(id);
    }

    // 本データの更新
    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public Book update(@PathVariable Integer id, @RequestBody Book req) {
        return bookService.update(id, req);
    }

    @GetMapping
    public String showLists(Model model) {
        model.addAttribute("books", bookService.getAllBooks());
        return "book/list";
    }
}