// This file contains Pseudocade, that should demonstrate, how users request and provide energy to the broker

/*
B_act:      actual battery status
B_tar:      target battery status
E_p:        energy production
E_c:        energy consumption
B_diff_req: required battery difference
B_diff_pro: provided battery difference
B_c:        Battery charge. How much Energy 1% stored Battery power provides in Watt. E.g: 1% ^= 100W 

 */


    static int B_c = 100;

main(){
    int B_diff_req;
    int B_act;
    int B_tar;          //read from data    Batterie Sollwert
    int E_p;            //read from data    Energieproduktion
    int E_c;            //read from data    Energieverbrauch

    B_diff_req = B_act - B_tar + E_p + E_v;
    B_diff_pro = compensate(B_diff_req);
    B_act = B_act + E_p - E_c + B_diff_pro;
}

int compensate(int B_diff_req){
    int x;
    if(B_diff_req<0){
        x=request(B_diff_req/B_c);
    }else{
        x=provide(B_diff_req/B_c);
    }
    return(x*B_c + B_diff_req%B_c);
}

int request(int B_diff_req){
    int y,z;
    y=getAvailableEnergy();
    if(y>B_diff_req){
        z=requestEnergy(B_diff_req);
    }else{
        z=requestEnergy(y);
    }
    return z;       //should be a positive value
}

int provide(int B_diff_req){
    int z;
    z=provideEnergy(x);
    return z;       //should be a negative value
}

int requestEnergy(int value){
    //withdraws access energy from community/broker
}

int provideEnergy(int value){
    //offers access energy to community/broker
}


