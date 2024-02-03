using AutoMapper;
using IngresoCDA.Modelos;
using IngresoCDA.Modelos.DTO;


namespace IngresoCDA.MapeoModelos
{
    //you need to extend Profile (Inherit) this add AutoMapper
    public class MapeoModelos : Profile
    {
        //create class constructor using ctor
        public MapeoModelos()
        {
            //link using map
            //in the file Program.cs adding AutoMapper as a service
            CreateMap<PlanillaIngreso, PlantillaIngresoDTO>();
            CreateMap<PlantillaIngresoDTO, PlanillaIngreso>();
        }
    }
}
