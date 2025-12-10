clc;
clear;
close all;

%% --- Paramètres ---
csvFile = 'data.csv';  
shadingType = 'interp'; % 'flat', 'interp', ou 'faceted'

%% --- Lire les données ---
try
    M = readmatrix(csvFile);
catch
    error('Impossible de lire le fichier CSV. Vérifie le chemin et le format.');
end

% Vérifier la taille
if ~ismatrix(M) || size(M,1) ~= 8 || size(M,2) ~= 8
    warning('Le CSV n''est pas 8x8. Le script continue avec la taille trouvée.');
end

% Remplacer les zéros par NaN
M(M == 0) = NaN;

%% --- Création de la surface 3D ---
figure('Name','Visualisation 3D CSV','NumberTitle','off');

% Affichage 3D avec couleur uniforme (gris clair)
hSurf = surf(M, 'EdgeColor', 'none', 'FaceColor', [0.8 0.8 0.8]);

% Rendu lisse
shading(shadingType);

% Labels et titre
xlabel('X');
ylabel('Y');
zlabel('Valeur');
title('Visualisation 3D du fichier CSV');

% Vue et options
view(45, 30);
grid on;
axis tight;

%% --- Fin du script ---
disp('Affichage 3D terminé !');
