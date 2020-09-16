import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { TechComponent } from './components/news/tech/tech.component';
import { SoftwareComponent } from './components/jobs/software/software.component';

const routes: Routes = [
  {
    path:"home",
    component:HomeComponent
  },
  {
    path:"news/tech",
    component:TechComponent
  },
  {
    path:"jobs/software",
    component:SoftwareComponent
  },
  {
    path:"**",
    pathMatch:"full",
    redirectTo:"home"
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
