# Irregularidades

Funções de suporte aos dados de irregularidades dados como entrada no SIMPACK (arquivos .trm e .tre)

## Uso

Para construir o arquivo executável
```bash
make
```

Para gerar os arquivos
```bash
./irregularity <Parameters file>
```

## Arquivo contendo os parâmetros de entrada (Parameters file)
```c
char[]        ! Problem name
char[]        ! File with values (CSV, doubles separated by dot and columns separated by commas)
int           ! Column position of x (lat/long)
int           ! Column position of y (lat/long)
int           ! Column position of z (INCERTEZA)
int           ! Column position of u (Superelevação)
int           ! Column position of Delta-y l (ALLr)
int           ! Column position of Delta-y r (ALRr)
int           ! Column position of Delta-z l (NLE5r)
int           ! Column position of Delta-z r (NLD5r)
double	      ! Path size of s (Localizacao)
double        ! Length scaling factor for x, y, z (meters)
double        ! Length scaling factor for u (millimeters)
double        ! Superelevation about Track centerline -CHECK
double        ! Superelevation reference baselength (meters) -CHECK
double        ! Increment for data reduction
double        ! Length scaling factor for s (meters)
double        ! Length scaling factor for Delta-y left (meters)
double        ! Length scaling factor for Delta-y right (meters)
double        ! Length scaling factor for Delta-z left (meters)
double        ! Length scaling factor for Delta-z right (meters)
double        ! Increment for data reduction
```

#### Acerca da nomenclatura das colunas relacionadas à Track excitation:

##### Nivelamento = irregularidade vertical

NLE - nivelamento esquerdo

NLD - nivelamento direito

ALL - alinhamento esquerdo

ALR - alinhamento direito

##### Irregularidade lateral
L = left
R = right
