#pip install scikit-fuzzy
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
caloriasDia = ctrl.Antecedent(np.arange(0, 2501, 100), 'caloriasConsumidasDia')
horasExercicio = ctrl.Antecedent(np.arange(0, 4, 1), 'horasExercicio')

#Variaveis de saída (Consequent)
chancesObesidade = ctrl.Consequent(np.arange(0, 101, 1), 'chancesObesidade')

# automf -> Atribuição de categorias automaticamente
caloriasDia.automf(names=['Baixa','Media','Alta'],)
horasExercicio.automf(names=['Baixa','Razoavel','Bom'],)

# atribuicao sem o automf
chancesObesidade['Minima'] =  fuzz.gaussmf(chancesObesidade.universe, 0, 10)
chancesObesidade['Baixa'] =  fuzz.gaussmf(chancesObesidade.universe, 20, 10)
chancesObesidade['Media'] =  fuzz.gaussmf(chancesObesidade.universe, 40, 10)
chancesObesidade['Alta'] =  fuzz.gaussmf(chancesObesidade.universe, 60, 10)
chancesObesidade['Muito alta'] =  fuzz.gaussmf(chancesObesidade.universe, 80, 10)

#Visualizando as variáveis
caloriasDia.view()
chancesObesidade.view()

#Criando as regras
regra_1 = ctrl.Rule(caloriasDia['Baixa'] & horasExercicio['Baixa'], chancesObesidade['Baixa'])
regra_2 = ctrl.Rule(caloriasDia['Baixa'] & horasExercicio['Razoavel'], chancesObesidade['Minima'])
regra_3 = ctrl.Rule(caloriasDia['Baixa'] & horasExercicio['Bom'], chancesObesidade['Minima'])

regra_4 = ctrl.Rule(caloriasDia['Media'] & horasExercicio['Baixa'], chancesObesidade['Media'])
regra_5 = ctrl.Rule(caloriasDia['Media'] & horasExercicio['Razoavel'], chancesObesidade['Media'])
regra_6 = ctrl.Rule(caloriasDia['Media'] & horasExercicio['Bom'], chancesObesidade['Baixa'])

regra_7 = ctrl.Rule(caloriasDia['Alta'] & horasExercicio['Baixa'], chancesObesidade['Muito alta'])
regra_8 = ctrl.Rule(caloriasDia['Alta'] & horasExercicio['Razoavel'], chancesObesidade['Alta'])
regra_9 = ctrl.Rule(caloriasDia['Alta'] & horasExercicio['Bom'], chancesObesidade['Alta'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3, regra_4, regra_5, regra_6, regra_7, regra_8, regra_9])


#Simulando
CaluloObesidade = ctrl.ControlSystemSimulation(controlador)

qtdeCaloriasDia = float(input('Quantidades de calorias consumidas no dia: '))
qtdeHorasExercicioDia = float(input('Quantidade de horas de exercicio no dia: '))
CaluloObesidade.input['caloriasConsumidasDia'] = qtdeCaloriasDia
CaluloObesidade.input['horasExercicio'] = qtdeHorasExercicioDia
CaluloObesidade.compute()

chancesObesidadeResult = CaluloObesidade.output['chancesObesidade']

print("\nCalorias consumidas (dia) %5.2f \n Horas exercicio (dia) %5.2f \n Chances de %5.2f de ser obeso" %(
        qtdeCaloriasDia,
        qtdeHorasExercicioDia,
        chancesObesidadeResult))


caloriasDia.view(sim=CaluloObesidade)
horasExercicio.view(sim=CaluloObesidade)
chancesObesidade.view(sim=CaluloObesidade)

plt.show()