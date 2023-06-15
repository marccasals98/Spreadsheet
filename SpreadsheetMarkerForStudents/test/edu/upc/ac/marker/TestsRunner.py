# -*- coding: utf-8 -*-
import importlib

from ClasesCorrector import SuperClassForTests

class TestRunner:

    notas = {} #es un mapa <string (clase), float (puntos obtenidos)>

    def __init__(self):
        self.toBeRun = [
"edu.upc.etsetb.arqsoft.spreadsheet.marker.text_content_test.TextContentTest", \
"edu.upc.etsetb.arqsoft.spreadsheet.marker.number_content_test.NumberContentTest", \
"edu.upc.etsetb.arqsoft.spreadsheet.marker.formula_content_test.FormulaContentTest", \
"edu.upc.etsetb.arqsoft.spreadsheet.marker.dependent_cells_test.DependentCellsTest", \
"edu.upc.etsetb.arqsoft.spreadsheet.marker.circular_dependencies_test.CircularDependenciesTest", \
"edu.upc.etsetb.arqsoft.spreadsheet.marker.save_test.SaveTest", \
"edu.upc.etsetb.arqsoft.spreadsheet.marker.load_test.LoadTest" \
            ]
        self.porcentajes = [1.5,1.5,64.5,12.5,7.5,5,5]
        self.clasesAPorcentajes = {} #mapa <string (clase),float (porcentaje)>
        self.clases = [] #secuencia de clases test
        i=0

        for pkgClassName in self.toBeRun:
            c = self.get_class(pkgClassName)
            TestRunner.notas[c.__name__]=0.0
            self.clasesAPorcentajes[c.__name__]=self.porcentajes[i]
            TestRunner.notas[c.__name__] = 0.0
            i=i+1

    def show_grades(self):
        print("\n\n")
        SuperClassForTests.showAlldErrors()
        print("\n\n")
        notaFinal = 0.0
        for clase, nota in TestRunner.notas.items():
            notaParcial = nota * self.clasesAPorcentajes[clase] / 100.0
            notaFinal = notaFinal+notaParcial
            print(f"\n\nNota en clase {clase}: {format(nota,'.2f')} (Porcentaje en nota final: {self.clasesAPorcentajes[clase]}%). Contribucion a nota final: {format(notaParcial,'.2f')}")
        print(f"\nNOTA FINAL DE CORRECCIÓN AUTOMÁTICA: {format(notaFinal,'.2f')}");
        print("----------------- ------------------ ");

    def get_class(self, kls ):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = importlib.import_module(module)
        return getattr(m,parts[len(parts)-1])


    def runTestSuite(self):
        for testerClass in self.toBeRun:
            c = self.get_class(testerClass)
            b = c()
            methods =dir(c)
            #print(str(methods))
            #print(str(methods))
            obMethod = getattr(c,"setUpClass")
            obMethod()
            for method in methods:
                if method.startswith("test"):
                    obMethod = getattr(b,"setUp")
                    obMethod()
                    obMethod = getattr(b,method)
                    obMethod()
                    obMethod = getattr(b,"tearDown")
                    obMethod()
            obMethod = getattr(c,"tearDownClass")
            obMethod()
            TestRunner.notas[c.__name__]=getattr(c,"nota")
 
runner = TestRunner()
runner.runTestSuite()
runner.show_grades()
