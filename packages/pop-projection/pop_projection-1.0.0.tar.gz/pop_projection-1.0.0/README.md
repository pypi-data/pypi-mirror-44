# pop_projection

Projection of a population of a retirement plan consisting of :
- employees (actives and retirees)
- their spouses
- thier childrens


Given such population at the end of year 0, we compute, for each following year (year 1, year 2, ..., year 100, and at the end of that year), the number of individuals, that survived, died and quit the company (actives only)  and those that retired (actives only). In addition to that, new spouses, new children, and new actives are also generated using given laws.

The laws governing suchs movements are :

- law of mortality (mortality tables)
- law of quitting
- law of retirement (this one is in fact deterministic : retirement at some age , 60 for example)
- law of marriage
- law of birth
- law of replacement

This laws (except law of replacement) are passed as functions or as a tuple of two elements, the fist one is a function, and the second one is a list of its parameters. The names of this parameters must exist in the list of columns of the dataframes employees, spouses or children (depending on the law. See below).
if the law is passed as function only, the names of the parameters used in the signature of the function must exist in the list of columns of the dataframes employees, spouses or children (depending on the law. See below).

Law of replacement is passed as function.

**Parameters of laws**
- law of quitting --> parameters names are in the list of columns of employees.
- law of retirement --> parameters names are in the list of columns of employees.
- law of marriage --> parameters names are in the list of columns of employees.
- law of birth --> parameters names are in the list of columns of spouses.
- law of replacement has two parameters : 
    - a dic storing number of departures of year year_ by group (employees who retired, resigned or died in year year_)
    - year of departure

**Return values of laws**

- law of quitting --> probablity that the employee will quit before the end of the next year.
- law of retirement --> 1 if the employee will retire before the end of the next year, 0 otherwise.
- law of marriage --> probablity that the employee will marry before the end of the next year.
- law of birth --> probablity that the spouse (if female) or his wife will give birth before the end of the next year.
- law of replacement --> a list of employees to add to population. Each employee in this list is a dic with keys : 'key' (to uniquely define the employee), 'number' and 'data' (list of values that corresponds to columns in employee except id).

# Installation
```
pip install pop-projection
```
# Usage example

```
import pop_projection.Effectifs as eff
import pop_projection.Actuariat as act
import pandas as pd

# Define law of retirement
def law_ret1(age, Year_employment):
    if Year_employment < 2002:
        if age+1 >= 55:
            return True
        else:
            return False
    if Year_employment >= 2002:
        if age+1 >= 60:
            return True
        else:
            return False

# Define law of reignation
def law_resignation_1(age, sex):
    if age+1 >= 50 :
        return 0
    if sex == 'female':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    if sex == 'male':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    


# Define law of marriage
def law_mar1(age, sexe, typeAgent):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if sexe == 'male':
        if typeAgent=='active':
            if age >= 25 and age <= 54:
                return 0.095
            else :
                return 0
        else:
            return 0
    
    if sexe == 'female':
        if typeAgent=='active':
            if age >= 25 and age <= 54:
                return 0.15
            else :
                return 0
        else:
            return 0


# Define law of replacement   
def law_replacement1(departures_, year_):
    
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : key, number and data
        
    '''
    def nouveaux(g_):
        structure_nouveaux = {'1':[25,25,0.8],'2':[25,25,0.8],'3':[25,25,0.6],'4':[29,29,0.6],'5':[28,28,0.5,],
        '6':[28,28,0.5],'7':[33,33,0.5],'8':[38,38,0.5],'9':[38,38,0.5],'10':[47,47,0.5],'11':[49,49,0.5]}

        if str(g_) in structure_nouveaux:
            return structure_nouveaux[str(g_)]
        else:
            return [30, 30, 1.0]

    def taux_rempl(y, g_ = '0'):
        if y <= 3 :
            if str(g_) in ['1','2','3','5','6','7']:
                return 0.64
            else:
                return 1
        else:
            return 1

    new_employees = []

    for g in departures_:
        # add a male
        if nouveaux(g)[2] > 0:
            temp = {'key':'male_groupe_' + str(g) + 'year_' + str(year_), 
            'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[0]))]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key':'female_groupe_' + str(g) + 'year_' + str(year_), 
            'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[1]))]}
            new_employees.append(temp)
    
    return new_employees

# Path for input data
path ="./pop_projection/data/"

# Number of years to project
MAX_YEARS = 50

# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

# View existing mortality tables
print('Mortality tables : \n',list(act.mortality_tables.keys()))

# Add the 2009 usa table
table_usa_2009 = pd.read_csv("table_usa_2009.csv",sep=";", decimal = ",")
act.add_mortality_table('table_usa_2009', list(table_usa_2009['Lx']))

# Projection of population
numbers_ = eff.simulerEffectif(employees, spouses, children, 'table_usa_2009', MAX_YEARS, 
            law_retirement_= law_ret1, law_resignation_= law_resignation_1, 
            law_marriage_= (law_mar1, ['age', 'sex', 'type']), law_replacement_= law_replacement1)

# Global numbers
Effectifs = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_YEARS)

# Print some lines
print(Effectifs.head(10))

# Export Effectifs
Effectifs.to_csv('Effectifs_python.csv', sep = ';', index=False, decimal=',')

#Number of actives leaving population : deaths, resignations, and new retired
Leaving = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_YEARS)

#Print some lines
print(Leaving.head(10))

#Export Leaving
Leaving.to_csv('Sortants_python.csv', sep = ';', index=False, decimal=',')

#export projected employees
pd.DataFrame.from_dict(numbers_[0]).to_csv('employees_proj.csv', sep = ';', index=False, decimal=',')

#export projected spouses
pd.DataFrame.from_dict(numbers_[1]).to_csv('spouses_proj.csv', sep = ';', index=False, decimal=',')

#export projected children
pd.DataFrame.from_dict(numbers_[2]).to_csv('children_proj.csv', sep = ';', index=False, decimal=',')
```
# Other examples : 

[Plotting Evolution of Ages pyramid over years]( https://github.com/ateffal/pop_projection/blob/master/usage_examples/usage_example_1.md)

