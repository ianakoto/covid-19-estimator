import json
import math


def estimator(data):
      
      """ THis function computes the estimation of covid 19 infected patients
      
      input: data as a dict
      
      data : 1. region as a dict
                            region: i. name as string
                                    ii. avgAge as double
                                    iii. avgDailyIncomeInUSD as double
                                    iv. avgDailyIncomePopulation as double

             2. periodType as string
             3. timeToElapse as an int
             4. reportedCases as an int
             5. population as an int
             6. totalHospitalBeds: as an int

       returns   a dictionary of input data, impact as dict, and severImpact as dict    
      
       """
      
      # normalize timeToElapse to days
      ptype = data.periodType;
      new_timeToElapse = 0;
      if ptype == "months":
            new_timeToElapse = 30 * int(data.timeToElapse);
      elif ptype == "weeks":
            new_timeToElapse = 7 * int(data.timeToElapse);
      else:
            new_timeToElapse = int(data.timeToElapse);
      
      factor = new_timeToElapse // 3;
            

      impact = {}
      severeImpact = {}

      impact['currentlyInfected'] = math.floor( int(data.reportedCases) * 10);
      severeImpact['currentlyInfected'] = math.floor(int(data.reportedCases) * 50);
     

      est_infectedPeople_impact =math.floor( impact['currentlyInfected'] * (2 * factor)); 
      est_infectedPeople_severeImpact = math.floor(severeImpact['currentlyInfected'] * (2 * factor));
      
      impact['infectionsByRequestedTime'] = est_infectedPeople_impact;
      severeImpact['infectionsByRequestedTime'] = est_infectedPeople_severeImpact;
      
      impact['severeCasesByRequestedTime'] =math.floor( (int(impact['infectionsByRequestedTime']) * 15) / 100);      
      severeImpact['severeCasesByRequestedTime'] =math.floor( (int(severeImpact['infectionsByRequestedTime']) * 15) / 100);

      totalHospitalBeds = (int(data.totalHospitalBeds) * 95) / 100;
      occupied_beds = (totalHospitalBeds * 65) / 100;
      unoccupied_beds_covid_patients = totalHospitalBeds - occupied_beds;

      impact['hospitalBedsByRequestedTime'] =math.floor( unoccupied_beds_covid_patients - impact['severeCasesByRequestedTime']);
      severeImpact['hospitalBedsByRequestedTime'] =math.floor( unoccupied_beds_covid_patients - severeImpact['severeCasesByRequestedTime']);

      impact['casesForICUByRequestedTime'] = math.floor((impact['infectionsByRequestedTime'] * 5) / 100);
      severeImpact['casesForICUByRequestedTime '] =math.floor( (severeImpact['infectionsByRequestedTime'] * 5) / 100);


      impact['casesForVentilatorsByRequestedTime'] =math.floor( (impact['infectionsByRequestedTime'] * 2) / 100);
      severeImpact['casesForVentilatorsByRequestedTime'] =math.floor( (severeImpact['infectionsByRequestedTime'] * 2) / 100);

      
      daily_income = data.region['avgDailyIncomeInUSD'];
      avd_income_population = data.region['avgDailyIncomePopulation'];
      


      impact['dollarsInFlight'] =math.floor( impact['infectionsByRequestedTime'] * daily_income * avd_income_population * new_timeToElapse);  
      severeImpact['severeCasesByRequestedTime'] =math.floor( severeImpact['infectionsByRequestedTime'] * daily_income * avd_income_population * new_timeToElapse);

      output = {'impact':impact,'severeImpact':severeImpact};


      return {'estimate': output}
      
       
