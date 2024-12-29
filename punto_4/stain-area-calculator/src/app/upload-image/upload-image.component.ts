import { Component, ViewChild, ElementRef, AfterViewInit, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
  selector: 'app-upload-image',
  templateUrl: './upload-image.component.html',
  styleUrls: ['./upload-image.component.css'],
  imports: [CommonModule, FormsModule]

})
export class UploadImageComponent implements AfterViewInit {
  @ViewChild('imageCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;
  private ctx!: CanvasRenderingContext2D;
  imageLoaded = false;
  private platformId = inject(PLATFORM_ID);
  public showButton = false;
  public showSlider = false;
  private router = inject(Router);
  /** Number of random points generated for image processing. */
  public numberPoints = 100;
  /** Points array storing randomly generated coordinates. */
  public points: { x: number; y: number }[] = [];

  /**
   * Lifecycle hook called after view initialization.
   * Sets the 2D rendering context if running in a browser.
   */
  ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.ctx = this.canvasRef.nativeElement.getContext('2d')!;
    }
  }

  /**
   * Triggered when a file is selected. Handles reading and drawing the image, then converts it to binary format.
   */
  onFileSelected(event: Event) {
    if (!isPlatformBrowser(this.platformId)) return;

    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const reader = new FileReader();

      reader.onload = (e: ProgressEvent<FileReader>) => {
        const img = new Image();
        img.onload = () => {
          this.canvasRef.nativeElement.width = img.width;
          this.canvasRef.nativeElement.height = img.height;
          this.ctx.drawImage(img, 0, 0);
          this.convertToBinary();
          this.imageLoaded = true;
          this.showButton = true;
          this.showSlider = true;
          this.points = this.generateRandomPoints(this.numberPoints);
        };
        img.src = (e.target as FileReader).result as string;
      };

      reader.readAsDataURL(input.files[0]);
    }
  }

  /**
   * Navigates to the calculation route, passing along the image data and random points.
   */
  navigateToCalculate() {
    const imageData = this.canvasRef.nativeElement.toDataURL('image/png');
    this.router.navigate(['/calculate'], {
      state: { Image: imageData, points: this.points },
    });
  }

  /**
   * Converts the displayed image to a binary (black/white) representation.
   */
  private convertToBinary() {
    const imageData = this.ctx.getImageData(0, 0, this.canvasRef.nativeElement.width, this.canvasRef.nativeElement.height);
    const binaryData = new Uint8ClampedArray(imageData.data);

    for (let i = 0; i < binaryData.length; i += 4) {
      const grayscale = 0.3 * binaryData[i] + 0.59 * binaryData[i + 1] + 0.11 * binaryData[i + 2];
      const binaryValue = grayscale > 128 ? 255 : 0;
      binaryData[i] = binaryData[i + 1] = binaryData[i + 2] = binaryValue; // Blanco o negro
      binaryData[i + 3] = 255; // Alpha
    }

    this.ctx.putImageData(new ImageData(binaryData, this.canvasRef.nativeElement.width, this.canvasRef.nativeElement.height), 0, 0);
  }

  /**
   * Generates 'n' random points within the canvas boundaries.
   */
  private generateRandomPoints(n: number): { x: number; y: number }[] {
    const points = [];
    const width = this.canvasRef.nativeElement.width;
    const height = this.canvasRef.nativeElement.height;

    for (let i = 0; i < n; i++) {
      points.push({
        x: Math.floor(Math.random() * width),
        y: Math.floor(Math.random() * height),
      });
    }

    return points;
  }

  /**
   * Updates the number of points whenever the slider value changes, then re-generates the points.
   */
  onSliderChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.numberPoints = parseInt(value);
    this.points = this.generateRandomPoints(this.numberPoints);
  }

}