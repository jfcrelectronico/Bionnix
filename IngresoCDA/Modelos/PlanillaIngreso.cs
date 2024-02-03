using System.ComponentModel.DataAnnotations;//se importa para el uso de key

namespace IngresoCDA.Modelos
{
    public class PlanillaIngreso
    {
        [Key]
        public int Id { get; set; }
        [Required]
        public string CarId { get; set; }
        [Required]
        public string CarOwner { get; set; }
        [Required]
        public string CarOwnerAdd { get; set; }
        [Required]
        public string WheelSize { get; set; }
        [Required]
        public string ChassNum { get; set; }
        [Required]
        public string EngineNum { get; set; }
        [Required]
        public string CarKm { get; set; }
        [Required]
        public string YearMade { get; set; }
        [Required]
        public string CarType { get; set; }
        [Required]
        public string CarUse { get; set; }
        [Required]
        public string CarMenu { get; set; }
        [Required]
        public string CarModel { get; set; }
        [Required]
        public string EngineCode { get; set; }
        [Required]
        public string FuelType { get; set; }
        [Required]
        public string CarAxl { get; set; }
        [Required]
        public string ExpDate { get; set; }
        [Required]
        public string  TestDate { get; set; }
        [Required]
        public string Payment { get; set; }
        [Required]
        public string PAIS { get; set; }
        [Required]
        public string CIUDAD { get; set; }
        [Required]
        public string COD_CIUDAD { get; set; }
        [Required]
        public string DEPMTO { get; set; }
        [Required]
        public string Servicio { get; set; }
        [Required]
        public string CLASE { get; set; }
        [Required]
        public string MARCA { get; set; }
        [Required]
        public string COD_MARCA { get; set; }
        [Required]
        public string LINEA { get; set; }
        [Required]
        public string COD_LINEA { get; set; }
        [Required]
        public string LICENCIA { get; set; }
        [Required]
        public DateTime F_MATRICULA { get; set; } = DateTime.Now;

        [Required]
        public string COLOR { get; set; }
        [Required]
        public string COMBUSTIBLE { get; set; }
        [Required]
        public string VIN { get; set; }
        [Required]
        public string TIPO_MOTOR { get; set; }
        [Required]
        public string CILINDRAJE { get; set; }
        [Required]
        public string SILLAS { get; set; }
        [Required]
        public string POLARIZADO { get; set; }

        [Required]
        public string BLINDAJE { get; set; }
        [Required]
        public string TEL_OWNER { get; set; }
        [Required]
        public string CELULAR { get; set; }
        [Required]
        public string TIP_DOC { get; set; }
        [Required]
        public string N_DOC { get; set; }
        [Required]
        public string ASEGURADORA { get; set; }
        [Required]
        public string EXPIRA_SOAT { get; set; }
        [Required]
        public string CITY_OF_TEST { get; set; }
        [Required]
        public string FOTO { get; set; }

        [Required]
        public string OBSERVACIONES { get; set; }



    }
}
