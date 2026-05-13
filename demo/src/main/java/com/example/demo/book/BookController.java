package com.example.demo.book;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;
import org.springframework.stereotype.Controller;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.springframework.dao.EmptyResultDataAccessException;

@Controller
@RequestMapping("/books")
public class BookController {
    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    // データの登録
    @GetMapping("/register")
    public String showRegisterForm(Model model) {
        model.addAttribute("book", new Book());
        return "book/register";
    }

    @PostMapping("/register")
    public String register(@ModelAttribute Book book) {
        bookService.create(book);
        return "redirect:/books";
    }

    // データの削除
    @PostMapping("/delete/{id}")
    public String deleteById(@PathVariable Integer id, RedirectAttributes redirectAttributes) {
        try {
            bookService.deleteById(id);
            redirectAttributes.addFlashAttribute("successMessage", "Deleted book id=" + id);
        } catch (EmptyResultDataAccessException e) {
            redirectAttributes.addFlashAttribute("errorMessage", "Book not found: id=" + id);
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", "Failed to delete book id=" + id);
        }
        return "redirect:/books";
    }

    // データの更新
    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public Book update(@PathVariable Integer id, @RequestBody Book req) {
        return bookService.update(id, req);
    }

    // 一覧取得
    @GetMapping
    public String showLists(Model model) {
        model.addAttribute("books", bookService.getAllBooks());
        return "book/list";
    }

    // 詳細取得
    @GetMapping("/detail/{id}")
    public String detailBook(@PathVariable Integer id, Model model) {
        model.addAttribute("book", bookService.getById(id).orElse(null));
        return "book/detail";
    }
}
