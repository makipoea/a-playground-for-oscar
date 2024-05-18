#include <vtkSmartPointer.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkUnstructuredGrid.h>
#include <vtkDataSet.h>
#include <vtkPointData.h>
#include <vtkCellData.h>



int main(int argc, char* argv[])
{
    // Vérifiez que le chemin du fichier est passé en argument
    if (argc < 2)
    {
        std::cerr << "use " << argv[0] << " <filename.vtk>" << std::endl;
        return EXIT_FAILURE;
    }

   
    std::string filePath = argv[1];

    vtkSmartPointer<vtkUnstructuredGridReader> reader =  // quant un truc s'appelle smart il faut prendre peur  
        vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(filePath.c_str());
    reader->Update();

   
    vtkSmartPointer<vtkUnstructuredGrid> mesh = reader->GetOutput();

    std::cout << "Nombre de points : " << mesh->GetNumberOfPoints() << std::endl;
    std::cout << "Nombre de cellules : " << mesh->GetNumberOfCells() << std::endl;

    
    vtkDataSet* data = mesh;
    int numArrays = data->GetPointData()->GetNumberOfArrays();
    std::cout << "Nombre de champs de données associés aux points : " << numArrays << std::endl;

    for (int i = 0; i < numArrays; i++)
    {
        vtkDataArray* array = data->GetPointData()->GetArray(i);
        std::cout << "Nom du champ de données " << i + 1 << " : " << array->GetName() << std::endl;
        std::cout << "Taille du champ de données : " << array->GetNumberOfComponents() << " composants" << std::endl;
    }

    int numCellArrays = data->GetCellData()->GetNumberOfArrays();
    std::cout << "Nombre de champs de données associés aux cellules : " << numCellArrays << std::endl;

    for (int i = 0; i < numCellArrays; i++)
    {
        vtkDataArray* array = data->GetCellData()->GetArray(i);
        std::cout << "Nom du champ de données " << i + 1 << " : " << array->GetName() << std::endl;
        std::cout << "Taille du champ de données : " << array->GetNumberOfComponents() << " composants" << std::endl;
    }

    return EXIT_SUCCESS;
}
