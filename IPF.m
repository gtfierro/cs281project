function [logLhood Theta] = IPF(data, edges)
  % Implement the IPF algorithm in the pairwise Markov random field model
  % where the cliques are edges.

  % data is M-by-N, assumed binary
  % M is the number of nodes in the graph
  % N is the number of iid observations
  [M N] = size(data);
  % edges is a cell, each entry is of the form (s,t) for some 1 ≤ s < t ≤ N
  K = length(edges); % number of edges in the graph
  for k = 1:K % make sure s < t
      edges{k} = [edges{k,1}, edges{k,2}];
      %edges{k} = [min(edges{k}) max(edges{k})];
  end
  % Compute empirical distributions: Emp(i,j,k) is the fraction of the data
  % that has (X s, X t) = (i-1, j-1), where (s,t) = edges{k}.
  Emp = zeros(2,2,K);
  for k = 1:K
      % Find the nodes of the edge
      s = edges{k}(1);
      t = edges{k}(2);

      % Iterate over the observations and update the appropriate entry of Emp
      for n = 1:N
          i = data(s,n) + 1;
          j = data(t,n) + 1;
          Emp(i,j,k) = Emp(i,j,k) + 1/N;
      end
  end

  % Initialize the parameters: Theta(i,j,k) encodes theta st(X s=i-1,
      % X t=j-1), where (s,t) = edges{k}.
  Theta = zeros(2,2,K);

  % In this case the normalizer Z can be computed explicitly
  Z = 2^M;

  % Compute initial log likelihood
  logLhood = N*sum(sum(sum(Emp.*Theta))) - N*log(Z);

  % Iterate over all edges and configurations
  maxIter = 100; % maximum number of batch iterations
  for iter = 1:maxIter
  % Iterate over the edges
  for k = 1:K
  % Find the nodes of the edge
  s = edges{k}(1);
  t = edges{k}(2);

% Iterate over the configurations of (s,t)
  for i = 1:2
  for j = 1:2
  % Generate possible configurations for the remaining M-2
  % nodes.
% poss is 2ˆ(M-2)-by-(M-2)
  poss = generatePoss(M-2);

% Interleave with the configuration of (s,t)
  poss = [poss(:,1:s-1), ...
  (i-1) * ones(2^(M-2),1), ...
  poss(:,s:t-2), ...
  (j-1) * ones(2^(M-2),1), ...
  poss(:,t-1:end)];

  % Compute marginal probability by summing over all possibilities
  margPr = 0;
  for w = 1:size(poss,1)
  logPr = -log(Z);
  for e = 1:length(edges)
  logPr = logPr + ...
  Theta(poss(w,edges{e}(1))+1, poss(w,edges{e}(2))+1, e);
  end
  margPr = margPr + exp(logPr);
  end

  % Update the corresponding entry of Theta
  Theta(i,j,k) = Theta(i,j,k) + log(Emp(i,j,k)) - log(margPr);
  end
  end
  end

  % Compute log likelihood
  logOld = logLhood;
  logLhood = N*sum(sum(sum(Emp.*Theta))) - N*log(Z);

  % Check for convergence
if (logLhood - logOld < 1e-8)
  fprintf('Converges after %d batch iterations!\n', iter);
  break;
elseif (iter == maxIter)
  fprintf('IPF did not converge: final ∆ = %.8f\n', logLhood - logOld);
  end
  end


function poss = generatePoss(m)
  % Generates a (2ˆm)-by-m array consisting of all possible binary
  % configurations of m nodes.

if (m == 1)
  poss = [0; 1];
  else
  possRec = generatePoss(m-1);
  poss = [zeros(size(possRec,1),1), possRec; ...
  ones(size(possRec,1),1), possRec];
  end
