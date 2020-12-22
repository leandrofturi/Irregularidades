#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define SEP ","

typedef struct {
    double x, y, z, u;
} MeasuredTrack;

typedef struct {
    double s, Deltayl, Deltayr, Deltazl, Deltazr;
} TrackExcitation;


char* read_line(FILE *arq) {
    size_t n = 0, r;
    char *buf = NULL;

    r = getline(&buf, &n, arq);
    if(r < 0)
        return(NULL);

    if(buf && r >= UINT_MAX) {
        free(buf);
        return(NULL);
    }

    return(buf);
}


int main(int argc, char *argv[]) {
    const char* tok;
    char problem[251], filename_in[256], label[256], 
         *line;
    int i, colpos[8];
    double data[11], h;
    FILE *in, *trm, *tre;
    MeasuredTrack M;
    TrackExcitation T;

    if (argc < 2) {
		printf("Use ./irregularity <Parameters file>\n");
		exit(1);
	}

    // Leitura do arquivo de entrada
	if((in = fopen(argv[1], "r")) == NULL) {
		printf("File %s not found!\n", argv[1]);
		exit(1);
	}

    fscanf(in, "%s\t!%[^\n]\n", problem, label);
    fscanf(in, "%s\t!%[^\n]\n", filename_in, label);
    for(i = 0; i < 8; i++)
        fscanf(in, "%d\t!%[^\n]\n", &colpos[i], label);
    fscanf(in, "%lf\t!%[^\n]\n", &h, label);
    for(i = 0; i < 11; i++)
        fscanf(in, "%lf\t!%[^\n]\n", &data[i], label);

    fclose(in);

    // Arquivo .trm
	sprintf(label, "%s.trm", problem);
    if((trm = fopen(label, "w")) == NULL) {
		printf("Cant open %s!\n", label);
		exit(1);
	}

    fprintf(trm, "!\n");
    fprintf(trm, "! %s\n", problem);
    fprintf(trm, "! Measured Track: x, y, z and superelevation\n");
    fprintf(trm, "!\n");
    fprintf(trm, "\n");

    fprintf(trm, "header.begin\n");
    fprintf(trm, "   data.type\t=\t3\n"); // File format type: x, y, z, u
    fprintf(trm, "   data.par(1)\t=\t%.3lf\n", data[0]); // Length scaling factor for x, y, z (meters)
    fprintf(trm, "   data.par(2)\t=\t%.3lf\n", data[1]); // Length scaling factor for u (millimeters)
    fprintf(trm, "   data.par(4)\t=\t%.3lf\n", data[2]); // Superelevation about Track centerline
    fprintf(trm, "   data.par(5)\t=\t%.3lf\n", data[3]); // Superelevation reference baselength (meters)
    fprintf(trm, "   data.par(7)\t=\t%.3lf\n", data[4]); // Increment for data reduction
    fprintf(trm, "header.end\n");
    fprintf(trm, "\n");

    // Arquivo .tre
    sprintf(label, "%s.tre", problem);
    if((tre = fopen(label, "w")) == NULL) {
		printf("Cant open %s!\n", label);
		exit(1);
	}

    fprintf(tre, "!\n");
    fprintf(tre, "! %s\n", problem);
    fprintf(tre, "! Track excitation, rail related\n");
    fprintf(tre, "!\n");
    fprintf(tre, "\n");

    fprintf(tre, "header.begin\n");
    fprintf(tre, "   data.type\t=\t2\n"); // File format type: side or rail related
    fprintf(tre, "   data.par(1)\t=\t%.3lf\n", data[5]); // Length scaling factor for s (meters)
    fprintf(tre, "   data.par(2)\t=\t%.3lf\n", data[6]); // Length scaling factor for Delta-y left (meters)
    fprintf(tre, "   data.par(3)\t=\t%.3lf\n", data[7]); // Length scaling factor for Delta-y right (meters)
    fprintf(tre, "   data.par(4)\t=\t%.3lf\n", data[8]); // Length scaling factor for Delta-z left (meters)
    fprintf(tre, "   data.par(5)\t=\t%.3lf\n", data[9]); // Length scaling factor for Delta-z right (meters)
    fprintf(tre, "   data.par(6)\t=\t%.3lf\n", data[10]); //  Increment for data reduction
    fprintf(tre, "header.end\n");
    fprintf(tre, "\n");

    // Leitura do CSV e escrita das coordenadas
    if((in = fopen(filename_in, "r")) == NULL) {
		printf("File %s not found!\n", filename_in);
		exit(1);
	}

    // Leitura do CSV e escrita das coordenadas
    line = read_line(in); // Header
    free(line);

    T.s = 0;
    while(!feof(in)) {
        line = read_line(in);
        if(!line) continue;

        M.x = M.y = M.z = M.u = 0;
        T.Deltayl = T.Deltayr = T.Deltazl = T.Deltazr = 0;
        tok = strtok(line, SEP);

        for(i = 0; tok && *tok; i++) {
            if(i == colpos[0])
                M.x = strtod(tok, NULL);
            else if(i == colpos[1])
                M.y = strtod(tok, NULL);
            else if(i == colpos[2])
                M.z = strtod(tok, NULL);
            else if(i == colpos[3])
                M.u = strtod(tok, NULL);
            else if(i == colpos[4])
                T.Deltayl = strtod(tok, NULL);
            else if(i == colpos[5])
                T.Deltayr = strtod(tok, NULL);
            else if(i == colpos[6])
                T.Deltazl = strtod(tok, NULL);
            else if(i == colpos[7])
                T.Deltazr = strtod(tok, NULL);

            tok = strtok(NULL, SEP);
        }
        
        fprintf(trm, "   %.7e\t%.7e\t%.7e\t%.7e\n", M.x, M.y, M.z, M.u);
        fprintf(tre, "   %.7e\t%.7e\t%.7e\t%.7e\t%.7e\n", T.s, T.Deltayl, T.Deltayr, T.Deltazl, T.Deltazr);
        T.s += h;
        if(line) free(line);
    }

    fclose(trm);
    fclose(tre);

    return 0;
}