package com.example.demo.book;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;


@Entity
@Table(name = "books")
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(nullable = false, length = 255)
    private String author;

    private Integer volumes;

    @Column(name = "publisher", length = 255)
    private String publisher;

    @Column(length = 255)
    private String isbn;

    @Column(length = 255)
    private String genre;

    @Column(length = 255)
    private String status;

    @Column(name = "total_reading_time")
    private Integer totalReadingTime;

    @Column(name = "created_at", insertable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", insertable = false, updatable = false)
    private LocalDateTime updatedAt;

    @OneToMany(mappedBy = "book")
    private List<ReadingLog> readingLogs = new ArrayList<>();

    @OneToMany(mappedBy = "book")
    private List<Review> reviews = new ArrayList<>();

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getTitle() {return title; }
    public void setTitle(String title) { this.title = title; }
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    public Integer getVolumes() { return volumes; }
    public void setVolumes(Integer volumes) { this.volumes = volumes; }
    public String getPublisher() {return publisher; }
    public void setPublisher(String publisher) { this.publisher = publisher; }
    public String getIsbn() { return isbn; }
    public void setIsbn(String isbn) { this.isbn = isbn; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public void getTotalReadingTime(Integer totalReadingTime) { this.totalReadingTime = totalReadingTime; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}