import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

/**
 * Represents a point with x and y coordinates.
 */
interface Point {
  x: number;
  y: number;
}

/**
 * Input data for calculation.
 */
interface CalculationInput {
  points: Array<Point>;
  image: HTMLImageElement;
}

/**
 * Result of a calculation that includes area, points, and images.
 */
interface CalculationResult {
  area: number;
  points: Array<Point>;
  originalImage: HTMLImageElement;
  modifiedImage: HTMLImageElement;
}

/**
 * Provides methods to perform stain area calculations.
 */
@Injectable({
  providedIn: 'root'
})
export class CalculationService {
  private results = new BehaviorSubject<CalculationResult[]>([]);

  /**
   * Counts how many provided points lie inside the black stain area.
   * @param points An array of points to evaluate.
   * @param image The original image.
   * @returns Overlay image data and number of points inside.
   */
  private getPointsInside(points: Point[], image: HTMLImageElement): { overlayImageData: ImageData, pointsInside: number } {
    // Count points that are inside stain of the image
    const { overlayImageData, originalImageData } = this.overlayImage(image, points);
    let pointsInside = 0;
    for (let i = 0; i < overlayImageData.data.length; i += 4) {
      // Check if pixel is black in original and red in overlay
      if (originalImageData.data[i] === 0 &&
        originalImageData.data[i + 1] === 0 &&
        originalImageData.data[i + 2] === 0 &&
        overlayImageData.data[i] === 255 &&
        overlayImageData.data[i + 1] === 0 &&
        overlayImageData.data[i + 2] === 0) {
        pointsInside++;
      }
    }
    return { overlayImageData, pointsInside };
  }

  /**
   * Returns an observable of accumulated calculation results.
   * Performs area estimation and updates the list of results.
   * @param data Calculation input with points and image.
   */
  getResults(data: CalculationInput): Observable<CalculationResult[]> {
    if (!data.image) {
      throw new Error('Image is required for calculation');
    }
    if (!data.points || data.points.length < 3) {
      throw new Error('At least 3 points are required for calculation');
    }

    const totalArea = data.image.width * data.image.height;
    const { overlayImageData, pointsInside } = this.getPointsInside(data.points, data.image);
    const totalPoints = data.points.length;
    const estimatedArea = Number((totalArea * (pointsInside / totalPoints)).toFixed(4));

    // convert overlayImageData to HTMLImageElement
    const canvas = document.createElement('canvas');
    canvas.width = data.image.width;
    canvas.height = data.image.height;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Could not get canvas context');
    }
    ctx.putImageData(overlayImageData, 0, 0);
    const overlayImageDataUrl = canvas.toDataURL();
    const overlayImageDataImage = new Image();
    overlayImageDataImage.src = overlayImageDataUrl;
    overlayImageDataImage.width = data.image.width;
    overlayImageDataImage.height = data.image.height;


    const result: CalculationResult = {
      area: estimatedArea,
      points: data.points,
      originalImage: data.image,
      modifiedImage: overlayImageDataImage
    };

    this.addResult(result);
    return this.results.asObservable();
  }

  /**
   * Adds a new calculation result to the results list.
   * @param result The new calculation result.
   */
  addResult(result: CalculationResult): void {
    this.results.next([...this.results.value, result]);
  }

  /**
   * Overlays points on an image, returning both overlay and original image data.
   * @param image The original image.
   * @param points The points to draw.
   */
  overlayImage(image: HTMLImageElement, points: Point[]) {
    const canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Could not get canvas context');
    }
    ctx.drawImage(image, 0, 0);
    const originalImageData = ctx.getImageData(0, 0, image.width, image.height);


    // Draw points
    points.forEach(point => {
      ctx.beginPath();
      ctx.arc(point.x, point.y, 4, 0, 2 * Math.PI);
      ctx.fillStyle = 'rgba(255, 0, 0)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 0, 0)';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    const overlayImageData = ctx.getImageData(0, 0, image.width, image.height);
    return { overlayImageData, originalImageData };
  }
}
