from Model.with_beta import labda, zz, C_n2
from combined_fit.indices import scintillation_index, rytov_index_const
from formula.jitter import k

print(scintillation_index(rytov_index_const(k(labda), zz[-1], C_n2.mean())))
