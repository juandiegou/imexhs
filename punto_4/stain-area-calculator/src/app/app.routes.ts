import { Routes } from '@angular/router';
import { UploadImageComponent } from './upload-image/upload-image.component';
import { CalculateAreaComponent } from './calculate-area/calculate-area.component';
export const routes: Routes = [
    { path: 'upload', component: UploadImageComponent },
    { path: 'calculate', component: CalculateAreaComponent },
    { path: '', redirectTo: '/upload', pathMatch: 'full' }
];
