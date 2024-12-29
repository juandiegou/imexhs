import { Component } from '@angular/core';
import { CalculationService } from '../services/calculation.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

/**
 * Component responsible for calculating and displaying the area of a stain in an image
 * based on user-selected points. It receives image data and points through route navigation state.
 */
@Component({
  selector: 'app-calculate-area',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './calculate-area.component.html',
  styleUrl: './calculate-area.component.css'
})
export class CalculateAreaComponent {
  /** Stores the calculated area of the stain */
  public area: number = 0;

  /** Observable containing the calculation results */
  data$: any;

  /** The image being processed */
  private image: HTMLImageElement | null = null;

  /** Array of points selected by the user to define the stain area */
  private points: Array<{ x: number, y: number }> = [];

  /**
   * Initializes the component and processes navigation state data
   * @param calculationService Service for calculating the stain area
   * @param router Angular router for navigation handling
   */
  constructor(
    private calculationService: CalculationService,
    private router: Router
  ) {
    const navigation = this.router.getCurrentNavigation();
    const state = navigation?.extras?.state as any;

    // Process navigation state if image and points are available
    if (state?.Image && state?.points) {
      this.image = new Image();
      this.image.src = state.Image;
      this.points = state.points;

      // Calculate results when image loads
      this.image.onload = () => {
        this.data$ = this.calculationService.getResults({ image: this.image!, points: this.points });
      };
    } else {
      // Redirect to home if required data is missing
      setTimeout(() => {
        this.router.navigate(['/']);
      }, 5000);
    }
  }
}
