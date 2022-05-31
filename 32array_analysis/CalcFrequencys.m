function CalcFrequencys(arrayPoints, c)

    distances = pdist(arrayPoints) ; % Berechnung aller Entfernungen als Vektor

    dmin = min(distances); % Kleinste Entfernung im Array
    dmax = max(distances); % Größte Entfernung im Array

    fmax = c/(2*dmin); % fmax ,mindestens zwei Abtastpunkte pro Wellenlänge
    fmin = c/dmax; % Die Wellenlänge von fmin ist die größte Entfernung des Arrays

    fprintf('MaxFrequenzy: %f\n', fmax); 
    fprintf('MinFrequenzy: %f\n', fmin); 
    % Method output: MaxFrequenzy: 1372.800000
    %                MinFrequenzy: 242.679047
end

