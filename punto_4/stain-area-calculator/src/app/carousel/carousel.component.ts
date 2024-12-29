import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-carousel',
  imports: [CommonModule],
  templateUrl: './carousel.component.html',
  styleUrl: './carousel.component.css'
})
export class CarouselComponent {

  @Input() images: string[] = [];
  currentIndex = 0;

  /**
   * Moves the carousel to the previous slide.
   */
  prevSlide(): void {
    this.currentIndex =
      (this.currentIndex - 1 + this.images.length) % this.images.length;
  }

  /**
   * Moves the carousel to the next slide.
   */
  nextSlide(): void {
    this.currentIndex = (this.currentIndex + 1) % this.images.length;
  }

  /**
   * Moves the carousel to the slide with the given index.
   */
  goToSlide(index: number): void {
    this.currentIndex = index;
  }
}
