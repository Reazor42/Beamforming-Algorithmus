function [rm, coarray] = PlotCoArray(arrayPoints)
    arraySize = size(arrayPoints, 1);
    distances = zeros(arraySize*arraySize, 3);

    for i = 1:arraySize
        for j = 1:arraySize
            distances(j + (i-1)*arraySize, :) = arrayPoints(i,:) - arrayPoints(j,:);
        end
    end
    [C,~,ic] = unique(distances ,'rows');

    a_counts = accumarray(ic, 1);
    coarray = [C,a_counts];

     rm = (arraySize*arraySize)/(size(C,1));
     figure("Name",'Microphone Co-Array Geometry (in meter)')
     coarray = scatter(coarray(:,1), coarray(:,2), coarray(:,4)*10);
     fprintf('medium redundancy: %f\n', rm);
end

