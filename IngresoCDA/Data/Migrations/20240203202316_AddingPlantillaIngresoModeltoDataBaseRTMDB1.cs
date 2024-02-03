using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace IngresoCDA.Migrations
{
    /// <inheritdoc />
    public partial class AddingPlantillaIngresoModeltoDataBaseRTMDB1 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "PlanillaIngresos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CarId = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarOwner = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarOwnerAdd = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    WheelSize = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ChassNum = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    EngineNum = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarKm = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    YearMade = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarType = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarUse = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarMenu = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarModel = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    EngineCode = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    FuelType = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CarAxl = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ExpDate = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    TestDate = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Payment = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    PAIS = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CIUDAD = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    COD_CIUDAD = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    DEPMTO = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Servicio = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CLASE = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    MARCA = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    COD_MARCA = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    LINEA = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    COD_LINEA = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    LICENCIA = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    F_MATRICULA = table.Column<DateTime>(type: "datetime2", nullable: false),
                    COLOR = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    COMBUSTIBLE = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    VIN = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    TIPO_MOTOR = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CILINDRAJE = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    SILLAS = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    POLARIZADO = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    BLINDAJE = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    TEL_OWNER = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CELULAR = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    TIP_DOC = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    N_DOC = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ASEGURADORA = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    EXPIRA_SOAT = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CITY_OF_TEST = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    FOTO = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    OBSERVACIONES = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_PlanillaIngresos", x => x.Id);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "PlanillaIngresos");
        }
    }
}
