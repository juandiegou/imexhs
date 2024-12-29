import { Component, inject } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CarouselComponent } from './carousel/carousel.component';

/**
 * Root component of the Stain Area Calculator application.
 * Handles the main navigation and layout of the application.
 * @class AppComponent
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,
    CommonModule, CarouselComponent],
  templateUrl: './app.component.html',
})
export class AppComponent {
  /** Title of the application */
  title = 'stain-area-calculator';

  /** Current active tab in the application. Can be either 'upload' or 'calculate' */
  currentTab: 'upload' | 'calculate' = 'upload';

  /** Router service injection for navigation handling */
  private router = inject(Router);

  /** Array of image paths used in the methodology carousel */
  methodologyImages = [
    'assets/images/IMG_1.png',
    'assets/images/IMG_2.png',
    'assets/images/IMG_3.png',
    'assets/images/IMG_4.png',
    'assets/images/IMG_5.png',
    'assets/images/IMG_6.png'
  ];

  /**
   * Constructor initializes router subscription to track current route
   * and update the active tab accordingly.
   */
  constructor() {
    this.router.events.subscribe(() => {
      const currentRoute = this.router.url.split('/')[1] as 'upload' | 'calculate';
      if (currentRoute) {
        this.currentTab = currentRoute;
      }
    });
  }

  /**
   * Changes the active tab and navigates to the corresponding route
   * @param tab - The tab to navigate to ('upload' or 'calculate')
   */
  setTab(tab: 'upload' | 'calculate'): void {
    this.currentTab = tab;
    this.router.navigate(['/' + tab]);
  }

  /**
   * Checks if a given tab is currently active
   * @param tab - The tab to check
   * @returns boolean indicating if the tab is active
   */
  isActive(tab: string): boolean {
    return this.currentTab === tab;
  }
}

