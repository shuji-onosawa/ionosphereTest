#include <iostream>
#include <cmath>
#include <fstream>
#include <iomanip>

//Define Ion
typedef struct  
{
  char name[20];  
  double mass;
  double charge;
} ion_type;
const double massunit = 1.67e-27;
const double chargeunit = 1.6e-19;
const ion_type oxygen{"oxygen",16.0*massunit,chargeunit};
const ion_type proton{"proton",1.0*massunit,chargeunit};

////Parameter
//Graphs_file_name_param
const ion_type ion = oxygen;
const double electric_field = 1.0e-3;
const double init_v_perp_eV = 0.01;
const double init_v_para_eV = 0.01;
const double max_v_para_for_resonance_eV = 0.1;//速度で比較するために、プロトンを基準に設定。ここのパラメータだけは、入力エネルギーに対して。酸素だろうとプロトンの質量をもとに上限v_paraを設定。
const double occur_duration = 1.0;
const double occur_period = 1.0;//occur_period秒の間にoccur_duration秒共鳴加速が発生
const double accele_t_max = 9999.0;
//Graphs_file_No_name_param
const double L_shell = 10.0;
const double init_Inval_lat_deg = 75.0;
const double dx_para_grid = 1e3;//(m)
const double dt = 0.001;//(s)
const double T = 600.0;//(s) // Simulation duration
const int write_out_times = 10; // How many calculations do you write once (for time plot)?
const double enable_lat_decrease = 1.0;//If this is 1, you think effect of decrease invalid latitude. if this is 0, no effect.
////


//Input value adjustment
const double mass = ion.mass;
const double electric_acceleration = electric_field*ion.charge/mass;
const double init_v_perp = sqrt(init_v_perp_eV*(1.60218e-19)*2.0/mass);
const double init_v_para = sqrt(init_v_para_eV*(1.60218e-19)*2.0/mass);
const double max_v_para_for_resonance = sqrt(max_v_para_for_resonance_eV*(1.60218e-19)*2.0/massunit);
const double R_e = 6.3e6;
const double init_Inval_lat = init_Inval_lat_deg/180.0*3.141592;

double grad_field(double inval_lat){
    return 3.0*sin(inval_lat)*(5.0*sin(inval_lat)*sin(inval_lat)+3.0)
/(pow((1.0+3.0*sin(inval_lat)*sin(inval_lat)),1.5)*cos(inval_lat)*cos(inval_lat))
*(1.0/(R_e*L_shell));
}

double dlambda(double inval_lat){
    return 1.0/(R_e*L_shell*cos(inval_lat)*sqrt(1.0+3.0*sin(inval_lat)*sin(inval_lat)));
}

//Calculation
double dv_para(double v_perp, double v_para, double inval_lat) {
    return grad_field(inval_lat) * 0.5 * pow(v_perp, 2.0);
}

double dv_perp(double v_perp, double v_para, double t, double inival_lat) {
    double dv_perp_val = electric_acceleration - v_para / v_perp * dv_para(v_perp, v_para, inival_lat);
    if((v_para>max_v_para_for_resonance||fmod(t,occur_period)>occur_duration)||accele_t_max<t){
        dv_perp_val = - v_para / v_perp * dv_para(v_perp, v_para, inival_lat);
    }
    return dv_perp_val;
}

int main() {
    double v_perp = init_v_perp;
    double v_para = init_v_para;
    double v_para_prev_x = init_v_para;
    double t = 0.0;
    double inval_lat = init_Inval_lat;
    int write_out_count = 0;

    //Values for x direction plot
    double x_para = 0.0;
    double x_para_grid = dx_para_grid;
    double dx_para = 0.0;
    double t_per_para_grid = 0.0;
    double first_t_per_para_grid = 0.0;
    double first_v_para = 0.0;
    int firstcount_for_grid = 0;
    

    std::ofstream ofs_t("./data/result_t.csv");
    ofs_t << "time,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV,inval_lat" << std::endl;
    std::ofstream ofs_x("./data/result_x.csv");
    ofs_x << "x,time,relative_density,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV,energy,energy_density,inval_lat" << std::endl;

    
    while (t < T) {
        //RK4
        double k1_perp = dv_perp(v_perp, v_para, t, inval_lat);
        double k1_para = dv_para(v_perp, v_para, inval_lat);

        double k2_perp = dv_perp(v_perp + 0.5 * dt * k1_perp, v_para + 0.5 * dt * k1_para, t+0.5*dt, inval_lat);
        double k2_para = dv_para(v_perp + 0.5 * dt * k1_perp, v_para + 0.5 * dt * k1_para, inval_lat);

        double k3_perp = dv_perp(v_perp + 0.5 * dt * k2_perp, v_para + 0.5 * dt * k2_para, t+0.5*dt, inval_lat);
        double k3_para = dv_para(v_perp + 0.5 * dt * k2_perp, v_para + 0.5 * dt * k2_para, inval_lat);

        double k4_perp = dv_perp(v_perp + dt * k3_perp, v_para + dt * k3_para, t+dt, inval_lat);
        double k4_para = dv_para(v_perp + dt * k3_perp, v_para + dt * k3_para, inval_lat);
        v_perp += dt / 6.0 * (k1_perp + 2.0 * k2_perp + 2.0 * k3_perp + k4_perp);
        v_para += dt / 6.0 * (k1_para + 2.0 * k2_para + 2.0 * k3_para + k4_para);
        t += dt;
        dx_para= v_para*dt;
        //End RK4

        //RK4 for lambda
        double k1_lambda = dlambda(inval_lat);
        double k2_lambda = dlambda(inval_lat - 0.5 * dx_para * k1_lambda);
        double k3_lambda = dlambda(inval_lat - 0.5 * dx_para * k2_lambda);
        double k4_lambda = dlambda(inval_lat - dx_para * k3_lambda);
        inval_lat -= dx_para / 6.0 * (k1_lambda + 2.0 * k2_lambda + 2.0 * k3_lambda + k4_lambda);

        //WriteOut section(Time plot)
        double pitch_angle = atan2(v_perp,v_para)*180/(3.1415926535);
        double v_perp_eV = 0.5*mass*v_perp*v_perp/(1.60218e-19);
        double v_para_eV = 0.5*mass*v_para*v_para/(1.60218e-19);

        write_out_count += 1;
        if(write_out_count>write_out_times){
            ofs_t << t << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << "," << inval_lat/3.14159265*180 << std::endl;
            write_out_count = 0;
        }

        //WriteOut section(x plot)
        x_para += fabs(dx_para);
        t_per_para_grid += dt;
        if(x_para>x_para_grid){
            if(firstcount_for_grid == 0){
                first_t_per_para_grid = t_per_para_grid;
                first_v_para = fabs(v_para);
                firstcount_for_grid += 1;
            }

            x_para_grid += dx_para_grid;
            int proceed_count = 1;
            while (x_para>x_para_grid)
            {
                x_para_grid += dx_para_grid;
                proceed_count++;
            }
            double dv_paradx = abs(v_para-v_para_prev_x);
            
            ofs_x << x_para_grid/1e3 << "," << t << "," << 1.0/(v_para/first_v_para) << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << "," << v_para_eV+v_perp_eV << "," << (v_para_eV+v_perp_eV)*t_per_para_grid/first_t_per_para_grid << "," << inval_lat/3.141592*180.0 << std::endl;
            // flux = constant, so 1/v_para = relative_density, I think

            // prev ver relative_density (It's wrong)
            // t_per_para_grid/first_t_per_para_grid

            v_para_prev_x = v_para;
            t_per_para_grid = 0.0;
        }

    }
    ofs_t.close();
    ofs_x.close();

    //Send parameter to Python
    int outdigit = 2;
    std::stringstream ss1, ss2, ss3, ss4, ss5, ss6, ss7;
    ss1 << std::fixed << std::setprecision(outdigit) << init_v_para_eV;
    std::string init_v_para_ev_str =ss1.str(); 
    ss2 << std::fixed << std::setprecision(outdigit) << init_v_perp_eV;
    std::string init_v_perp_ev_str =ss2.str(); 
    ss3 << std::fixed << std::setprecision(outdigit) << max_v_para_for_resonance_eV;
    std::string max_v_para_for_resonance_eV_str =ss3.str(); 
    ss4 << std::fixed << std::setprecision(outdigit) << electric_field*1e3;
    std::string electric_field_str =ss4.str(); 
    ss5 << std::fixed << std::setprecision(outdigit) << occur_duration;
    std::string occur_duration_str =ss5.str(); 
    ss6 << std::fixed << std::setprecision(outdigit) << occur_period;
    std::string occur_period_str =ss6.str(); 
    ss7 << std::fixed << std::setprecision(outdigit) << accele_t_max;
    std::string accele_t_max_str =ss7.str(); 

    std::ofstream ofs("./data/params.txt");
    ofs << ion.name << std::endl;
    ofs << init_v_para_ev_str << std::endl;
    ofs << init_v_perp_ev_str << std::endl;
    ofs << max_v_para_for_resonance_eV_str << std::endl;
    ofs << electric_field_str << std::endl;
    ofs << occur_duration_str << std::endl;
    ofs << occur_period_str << std::endl;
    ofs << accele_t_max_str << std::endl;
    ofs.close();


    //Execute Python
    std::string command = "python3 ./src/plot.py ";
    std::system(command.c_str());

    return 0;

}