package com.example.demo.book;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "reading_log")
public class ReadingLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "book_id")
    private Book book;

    @Column(length = 255)
    private String memo;

    @Column(name = "reading_time")
    private Integer readingTime;

    @Column(name = "reading_date", insertable = false, updatable = false)
    private LocalDateTime readingDate;

    @Column(name = "created_at", insertable = false, updatable = false)
    private LocalDateTime createdAt;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public Book getBook() {return book;}
    public void setBook(Book book) { this.book = book; }
    public String getMemo() { return memo; }
    public void setMemo(String memo) { this.memo = memo; }
    public Integer getReadingTime() { return readingTime; }
    public void setReadingTime(Integer readingTime) { this.readingTime = readingTime; }
    public LocalDateTime getReadingDate() { return readingDate; }
    public LocalDateTime getcreatedAt() { return createdAt; }
}