// This file contains Pseudocade, that should demonstrate, how users request and provide energy to the bank

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
    int B_diff_req;
    int B_act;
    int B_tar;          //read from data    Batterie Sollwert
    int E_p;            //read from data    Energieproduktion
    int E_c;            //read from data    Energieverbrauch


//-->call main every timestamp
main(){
    B_diff_req = B_act - B_tar + E_p - E_v;
    compensate(B_diff_req);
    //wait for callback
}

//Callback function. Subscribted to an event sent by bank
void response_bank(int B_diff_pro){
    B_act = B_act + E_p - E_c + B_diff_pro;
    //-->print B_act to plot
}


void compensate(int B_diff_req){
    if(B_diff_req<0){
        requestEnergy(B_diff_req);
    }else{
        provideEnergy(B_diff_req);
    }

}


void requestEnergy(int value){
    //sends a quantitative request to the bank waiting for reply
    /*
    Keyword "requestEnergy"
    Amount "value"
     */
    
}

void provideEnergy(int value){
    //sends a quantitative offer to the bank waiting for reply
    /*
    Keyword "provideEnergy"
    Amount "value"
     */
}


