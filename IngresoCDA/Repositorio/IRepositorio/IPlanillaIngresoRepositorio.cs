using IngresoCDA.Modelos.DTO;

namespace IngresoCDA.Repositorio.IRepositorio
{
    public interface IPlanillaIngresoRepositorio
    {
        //traer todos los registros existentes de la tabla PlantillaIngreso a traves del DTO usando Mapper
        public Task<IEnumerable<PlantillaIngresoDTO>> GetAllPlantillaIngreso();
        //traer solo el registro de la placa indicada
        public Task<PlantillaIngresoDTO> GetPlantillaIngreso(string CardId);
        //crear un nuevo registro recibe un objeto del tipo PlantillaIngresoDTO
        public Task<PlantillaIngresoDTO> CrearRegistroPlantillaIngreso(PlantillaIngresoDTO plantillaIngresoDTO);
        //actualizar un registro recibe el la placa y el objeto del tipo PlantillaIngresoDTO
        public Task<PlantillaIngresoDTO> ActualizarRegistroPlantillaIngreso(string CardId, PlantillaIngresoDTO plantillaIngresoDTO);
        //verificar si ya existe una placa igual ingresada actualmente en la tabla
        public Task<PlantillaIngresoDTO> PlacaExistePlantillaIngreso(string CardId);
        //borrar una placa de la tabla
        public Task<PlantillaIngresoDTO> BorrarPlacaPlantillaIngreso(string CardId);

        //traer todas la placa en una lista desplegable
        public Task<IEnumerable<PlantillaIngresoDTO>> GetDropDownPlantillaIngreso();
    }
}
