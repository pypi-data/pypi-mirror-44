/*
 * Normaliz
 * Copyright (C) 2007-2014  Winfried Bruns, Bogdan Ichim, Christof Soeger
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * As an exception, when this program is distributed through (i) the App Store
 * by Apple Inc.; (ii) the Mac App Store by Apple Inc.; or (iii) Google Play
 * by Google Inc., then that store may impose any digital rights management,
 * device limits and/or redistribution restrictions that are required by its
 * terms of service.
 */

#include <list>

#include "libnormaliz/vector_operations.h"
#include "libnormaliz/map_operations.h"
#include "libnormaliz/convert.h"
#include "libnormaliz/cone.h"
#include "libnormaliz/full_cone.h"

namespace libnormaliz {
using namespace std;

// adds the signs inequalities given by Signs to Inequalities
template<typename Integer>
Matrix<Integer> sign_inequalities(const vector< vector<Integer> >& Signs) {
    if (Signs.size() != 1) {
        errorOutput() << "ERROR: Bad signs matrix, has "
                      << Signs.size() << " rows (should be 1)!" << endl;
        throw BadInputException();
    }
    size_t dim = Signs[0].size();
    Matrix<Integer> Inequ(0,dim);
    vector<Integer> ineq(dim,0);
    for (size_t i=0; i<dim; i++) {
        Integer sign = Signs[0][i];
        if (sign == 1 || sign == -1) {
            ineq[i] = sign;
            Inequ.append(ineq);
            ineq[i] = 0;
        } else if (sign != 0) {
            errorOutput() << "ERROR: Bad signs matrix, has entry "
                          << sign << " (should be -1, 1 or 0)!" << endl;
            throw BadInputException();
        }
    }
    return Inequ;
}

template<typename Integer>
Matrix<Integer> strict_sign_inequalities(const vector< vector<Integer> >& Signs) {
    if (Signs.size() != 1) {
        errorOutput() << "ERROR: Bad signs matrix, has "
                      << Signs.size() << " rows (should be 1)!" << endl;
        throw BadInputException();
    }
    size_t dim = Signs[0].size();
    Matrix<Integer> Inequ(0,dim);
    vector<Integer> ineq(dim,0);
    ineq[dim-1]=-1;
    for (size_t i=0; i<dim-1; i++) {    // last component of strict_signs always 0
        Integer sign = Signs[0][i];
        if (sign == 1 || sign == -1) {
            ineq[i] = sign;
            Inequ.append(ineq);
            ineq[i] = 0;
        } else if (sign != 0) {
            errorOutput() << "ERROR: Bad signs matrix, has entry "
                          << sign << " (should be -1, 1 or 0)!" << endl;
            throw BadInputException();
        }
    }
    return Inequ;
}

template<typename Integer>
vector<vector<Integer> > find_input_matrix(const map< InputType, vector< vector<Integer> > >& multi_input_data,
                               const InputType type){

    typename map< InputType , vector< vector<Integer> > >::const_iterator it;
    it = multi_input_data.find(type);
    if (it != multi_input_data.end())
        return(it->second);

     vector< vector<Integer> > dummy;
     return(dummy);
}

template<typename Integer>
void insert_column(vector< vector<Integer> >& mat, size_t col, Integer entry){

    vector<Integer> help(mat[0].size()+1);
    for(size_t i=0;i<mat.size();++i){
        for(size_t j=0;j<col;++j)
            help[j]=mat[i][j];
        help[col]=entry;
        for(size_t j=col;j<mat[i].size();++j)
            help[j+1]=mat[i][j];
        mat[i]=help;
    }
}

template<typename Integer>
void insert_zero_column(vector< vector<Integer> >& mat, size_t col){
    // Integer entry=0;
    insert_column<Integer>(mat,col,0);
}

template<typename Integer>
void Cone<Integer>::homogenize_input(map< InputType, vector< vector<Integer> > >& multi_input_data){

    typename map< InputType , vector< vector<Integer> > >::iterator it;
    it = multi_input_data.begin();
    for(;it!=multi_input_data.end();++it){
        switch(it->first){
            case Type::dehomogenization:
                errorOutput() << "dehomogenization not allowed with inhomogeneous input!"<< endl;
                throw BadInputException();
                break;
            case Type::inhom_inequalities: // nothing to do
            case Type::inhom_equations:
            case Type::inhom_congruences:
            case Type::polyhedron:
            case Type::vertices:
            case Type::support_hyperplanes:
            case Type::grading:  // already taken care of
                break;
            case Type::strict_inequalities:
                insert_column<Integer>(it->second,dim-1,-1);
                break;
            case Type::offset:
                insert_column<Integer>(it->second,dim-1,1);
                break;
            default:  // is correct for signs and strict_signs !
                insert_zero_column<Integer>(it->second,dim-1);
                break;
        }
    }
}

//---------------------------------------------------------------------------

template<typename Integer>
Cone<Integer>::Cone(InputType input_type, const vector< vector<Integer> >& Input) {
    // convert to a map
    map< InputType, vector< vector<Integer> > > multi_input_data;
    multi_input_data[input_type] = Input;
    process_multi_input(multi_input_data);
}

template<typename Integer>
Cone<Integer>::Cone(InputType type1, const vector< vector<Integer> >& Input1,
                    InputType type2, const vector< vector<Integer> >& Input2) {
    if (type1 == type2) {
        errorOutput() << "Input types must be pairwise different!"<< endl;
        throw BadInputException();
    }
    // convert to a map
    map< InputType, vector< vector<Integer> > > multi_input_data;
    multi_input_data[type1] = Input1;
    multi_input_data[type2] = Input2;
    process_multi_input(multi_input_data);
}

template<typename Integer>
Cone<Integer>::Cone(InputType type1, const vector< vector<Integer> >& Input1,
                    InputType type2, const vector< vector<Integer> >& Input2,
                    InputType type3, const vector< vector<Integer> >& Input3) {
    if (type1 == type2 || type1 == type3 || type2 == type3) {
        errorOutput() << "Input types must be pairwise different!"<< endl;
        throw BadInputException();
    }
    // convert to a map
    map< InputType, vector< vector<Integer> > > multi_input_data;
    multi_input_data[type1] = Input1;
    multi_input_data[type2] = Input2;
    multi_input_data[type3] = Input3;
    process_multi_input(multi_input_data);
}

template<typename Integer>
Cone<Integer>::Cone(const map< InputType, vector< vector<Integer> > >& multi_input_data) {
    process_multi_input(multi_input_data);
}

//---------------------------------------------------------------------------


template<typename Integer>
void Cone<Integer>::process_multi_input(const map< InputType, vector< vector<Integer> > >& multi_input_data_const) {
    initialize();
    map< InputType, vector< vector<Integer> > > multi_input_data(multi_input_data_const);
    typename map< InputType , vector< vector<Integer> > >::iterator it=multi_input_data.begin();
    // find basic input type
    bool lattice_ideal_input=false;
    bool inhom_input=false;
    size_t nr_latt_gen=0, nr_cone_gen=0;

    // remove empty matrices
    it = multi_input_data.begin();
    for(; it != multi_input_data.end();) {
        if (it->second.size() == 0)
            multi_input_data.erase(it++);
        else
            ++it;
    }

    if(multi_input_data.size()==0){
        errorOutput() << "All input matrices empty!"<< endl;
        throw BadInputException();
    }


    it = multi_input_data.begin();
    for(; it != multi_input_data.end(); ++it) {
        switch (it->first) {
            case Type::inhom_inequalities:
            case Type::inhom_equations:
            case Type::inhom_congruences:
            case Type::strict_inequalities:
            case Type::strict_signs:
                inhom_input=true;
            case Type::signs:
            case Type::inequalities:
            case Type::equations:
            case Type::congruences:
                break;
            case Type::lattice_ideal:
                lattice_ideal_input=true;
                break;
            case Type::polyhedron:
                inhom_input=true;
            case Type::integral_closure:
            case Type::rees_algebra:
            case Type::polytope:
            case Type::cone:
                nr_cone_gen++;
                break;
            case Type::normalization:
            case Type::cone_and_lattice:
                nr_cone_gen++;
            case Type::lattice:
            case Type::saturation:
                nr_latt_gen++;
                break;
            case Type::vertices:
            case Type::offset:
                inhom_input=true;
            default:
                break;
        }

    }

    if(nr_cone_gen>1){
        errorOutput() << "Only one matrix of cone generators allowed!" << endl;
        throw BadInputException();
    }
    if(nr_latt_gen>1){
        errorOutput() << "Only one matrix of lattice generators allowed!" << endl;
        throw BadInputException();
    }
    if(lattice_ideal_input){
        if(multi_input_data.size() > 2 || (multi_input_data.size()==2 && !exists_element(multi_input_data,Type::grading))){
            errorOutput() << "Only grading allowed with lattice_ideal!" << endl;
            throw BadInputException();
        }
    }
    if(inhom_input){
        if(exists_element(multi_input_data,Type::dehomogenization) || exists_element(multi_input_data,Type::support_hyperplanes)){
            errorOutput() << "dehomogenizaion and support_hyperplanes not allowed with inhomogeneous input!" << endl;
            throw BadInputException();
        }
    }
    if(inhom_input || exists_element(multi_input_data,Type::dehomogenization)){
        if(exists_element(multi_input_data,Type::rees_algebra) || exists_element(multi_input_data,Type::polytope)){
            errorOutput() << "polytope and rees_algebra not allowed with inhomogeneous input or hehomogenizaion!" << endl;
            throw BadInputException();
        }
        if(exists_element(multi_input_data,Type::excluded_faces)){
            errorOutput() << "excluded_faces not allowed with inhomogeneous input or dehomogenizaion!"<< endl;
            throw BadInputException();
        }
    }
    if(exists_element(multi_input_data,Type::grading) && exists_element(multi_input_data,Type::polytope)){
           errorOutput() << "No explicit grading allowed with polytope!" << endl;
           throw BadInputException();                     
    }

    //determine dimension
    it = multi_input_data.begin();
    size_t inhom_corr = 0; // correction in the inhom_input case
    if (inhom_input) inhom_corr = 1;
    dim = it->second.front().size() - type_nr_columns_correction(it->first) + inhom_corr;

    // We now process input types that are independent of generators, constraints, lattice_ideal

    // check for excluded faces
    ExcludedFaces = find_input_matrix(multi_input_data,Type::excluded_faces);
    PreComputedSupportHyperplanes = find_input_matrix(multi_input_data,Type::support_hyperplanes);

    // check for a grading
    vector< vector<Integer> > lf = find_input_matrix(multi_input_data,Type::grading);
    if (lf.size() > 1) {
        errorOutput() << "ERROR: Bad grading, has "
                      << lf.size() << " rows (should be 1)!" << endl;
        throw BadInputException();
    }
    if(lf.size()==1){
        if(inhom_input)
            lf[0].push_back(0); // first we extend grading trivially to have the right dimension
        setGrading (lf[0]);     // will eventually be set in full_cone.cpp

    }

    // cout << "Dim " << dim <<endl;

    // check consistence of dimension
    it = multi_input_data.begin();
    size_t test_dim;
    for (; it != multi_input_data.end(); ++it) {
        test_dim = it->second.front().size() - type_nr_columns_correction(it->first) + inhom_corr;
        if (test_dim != dim) {
            errorOutput() << "Inconsistent dimensions in input!"<< endl;
            throw BadInputException();
        }
    }

    if(inhom_input)
        homogenize_input(multi_input_data);

    // check for a dehomogenization
    lf = find_input_matrix(multi_input_data,Type::dehomogenization);
    if (lf.size() > 1) {
        errorOutput() << "ERROR: Bad dehomogenization, has "
        << lf.size() << " rows (should be 1)!" << endl;
        throw BadInputException();
    }
    if(lf.size()==1){
        setDehomogenization(lf[0]);
    }

    // now we can unify implicit and explicit truncation
    // Note: implicit and explicit truncation have already been excluded
    if (inhom_input) {
        Dehomogenization.resize(dim,0),
        Dehomogenization[dim-1]=1;
        is_Computed.set(ConeProperty::Dehomogenization);
    }
    if(isComputed(ConeProperty::Dehomogenization))
        inhomogeneous=true;

    if(lattice_ideal_input){
        prepare_input_lattice_ideal(multi_input_data);
    }

    Matrix<Integer> LatticeGenerators(0,dim);
    prepare_input_generators(multi_input_data, LatticeGenerators);

    Matrix<Integer> Equations(0,dim), Congruences(0,dim+1);
    Matrix<Integer> Inequalities(0,dim);
    prepare_input_constraints(multi_input_data,Equations,Congruences,Inequalities);

    // set default values if necessary
    if(inhom_input && LatticeGenerators.nr_of_rows()!=0 && !exists_element(multi_input_data,Type::offset)){
        vector<Integer> offset(dim);
        offset[dim-1]=1;
        LatticeGenerators.append(offset);
    }
    if(inhom_input &&  Generators.nr_of_rows()!=0 && !exists_element(multi_input_data,Type::vertices) 
                && !exists_element(multi_input_data,Type::polyhedron)){
        vector<Integer> vertex(dim);
        vertex[dim-1]=1;
        Generators.append(vertex);
    }

    if(Inequalities.nr_of_rows()>0 && Generators.nr_of_rows()>0){ // eliminate superfluous inequalities
        vector<key_t> essential;
        for(size_t i=0;i<Inequalities.nr_of_rows();++i){
            for (size_t j=0;j<Generators.nr_of_rows();++j){
                if(v_scalar_product(Inequalities[i],Generators[j])<0){
                    essential.push_back(i);
                    break;
                }
            }
        }
        if(essential.size()<Inequalities.nr_of_rows())
            Inequalities=Inequalities.submatrix(essential);
    }

    // cout << "Ineq " << Inequalities.nr_of_rows() << endl;

    process_lattice_data(LatticeGenerators,Congruences,Equations);

    bool cone_sat_eq=no_lattice_restriction;
    bool cone_sat_cong=no_lattice_restriction;

    // cout << "nolatrest " << no_lattice_restriction << endl;

    if(Inequalities.nr_of_rows()==0 && Generators.nr_of_rows()!=0){
        if(!no_lattice_restriction){
            cone_sat_eq=true;
            for(size_t i=0;i<Generators.nr_of_rows() && cone_sat_eq;++i)
                for(size_t j=0;j<Equations.nr_of_rows()  && cone_sat_eq ;++j)
                    if(v_scalar_product(Generators[i],Equations[j])!=0){
                        cone_sat_eq=false;
            }
        }
        if(!no_lattice_restriction){
            cone_sat_cong=true;
            for(size_t i=0;i<Generators.nr_of_rows() && cone_sat_cong;++i){
                vector<Integer> test=Generators[i];
                test.resize(dim+1);
                for(size_t j=0;j<Congruences.nr_of_rows()  && cone_sat_cong ;++j)
                    if(v_scalar_product(test,Congruences[j]) % Congruences[j][dim] !=0)
                        cone_sat_cong=false;
            }
        }

        if(cone_sat_eq && cone_sat_cong){
            set_original_monoid_generators(Generators);
        }

        if(cone_sat_eq && !cone_sat_cong){ // multiply generators by anniullator mod sublattice
            for(size_t i=0;i<Generators.nr_of_rows();++i)
                v_scalar_multiplication(Generators[i],BasisChange.getAnnihilator());
            cone_sat_cong=true;
        }
    }

    if((Inequalities.nr_of_rows()!=0 || !cone_sat_eq) && Generators.nr_of_rows()!=0){
        Sublattice_Representation<Integer> ConeLatt(Generators,true);
        Full_Cone<Integer> TmpCone(ConeLatt.to_sublattice(Generators));
        TmpCone.dualize_cone();
        Inequalities.append(ConeLatt.from_sublattice_dual(TmpCone.Support_Hyperplanes));
        Generators=Matrix<Integer>(0,dim); // Generators now converted into inequalities
    }

    assert(Inequalities.nr_of_rows()==0 || Generators.nr_of_rows()==0);

    if(Generators.nr_of_rows()==0)
        prepare_input_type_4(Inequalities); // inserts default inequalties if necessary
    else{
        is_Computed.set(ConeProperty::Generators);
        is_Computed.set(ConeProperty::Sublattice);
    }

    WeightsGrad=Matrix<Integer> (0,dim);  // weight matrix for ordering
    if(isComputed(ConeProperty::Grading))
        WeightsGrad.append(Grading);
    GradAbs=vector<bool>(WeightsGrad.nr_of_rows(),false);

    if(PreComputedSupportHyperplanes.nr_of_rows()>0){
        check_precomputed_support_hyperplanes();
        SupportHyperplanes=PreComputedSupportHyperplanes;
        is_Computed.set(ConeProperty::SupportHyperplanes);
    }

    /* if(ExcludedFaces.nr_of_rows()>0){ // Nothing to check anymore
        check_excluded_faces();
    } */

    /*
    cout <<"-----------------------" << endl;
    cout << "Gen " << endl;
    Generators.pretty_print(cout);
    cout << "Supp " << endl;
    SupportHyperplanes.pretty_print(cout);
    cout << "A" << endl;
    BasisChange.get_A().pretty_print(cout);
    cout << "B" << endl;
    BasisChange.get_B().pretty_print(cout);
    cout <<"-----------------------" << endl;
    */
}


//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::prepare_input_constraints(const map< InputType, vector< vector<Integer> > >& multi_input_data,
    Matrix<Integer>& Equations, Matrix<Integer>& Congruences, Matrix<Integer>& Inequalities) {

    Matrix<Integer> Signs(0,dim), StrictSigns(0,dim);

    SupportHyperplanes=Matrix<Integer>(0,dim);

    typename map< InputType , vector< vector<Integer> > >::const_iterator it=multi_input_data.begin();

    it = multi_input_data.begin();
    for (; it != multi_input_data.end(); ++it) {

        switch (it->first) {
            case Type::strict_inequalities:
            case Type::inequalities:
            case Type::inhom_inequalities:
            case Type::excluded_faces:
                Inequalities.append(it->second);
                break;
            case Type::equations:
            case Type::inhom_equations:
                Equations.append(it->second);
                break;
            case Type::congruences:
            case Type::inhom_congruences:
                Congruences.append(it->second);
                break;
            case Type::signs:
                Signs = sign_inequalities(it->second);
                break;
            case Type::strict_signs:
                StrictSigns = strict_sign_inequalities(it->second);
                break;
            default:
                break;
        }
    }
    if(!BC_set) compose_basis_change(Sublattice_Representation<Integer>(dim));
    Matrix<Integer> Help(Signs);  // signs first !!
    Help.append(StrictSigns);   // then strict signs
    Help.append(Inequalities);
    Inequalities=Help;
}

//---------------------------------------------------------------------------
template<typename Integer>
void Cone<Integer>::prepare_input_generators(map< InputType, vector< vector<Integer> > >& multi_input_data, Matrix<Integer>& LatticeGenerators) {

    if(exists_element(multi_input_data,Type::vertices)){
        for(size_t i=0;i<multi_input_data[Type::vertices].size();++i)
            if(multi_input_data[Type::vertices][i][dim-1] <=0){
                errorOutput() << "Vertex has non-positive denominator!" << endl;
                throw BadInputException();
            }
    }

    if(exists_element(multi_input_data,Type::polyhedron)){
        for(size_t i=0;i<multi_input_data[Type::polyhedron].size();++i)
            if(multi_input_data[Type::polyhedron][i][dim-1] <0){
                errorOutput() << "Vertex has non-positive denominator!" << endl;
                throw BadInputException();
            }
    }

    typename map< InputType , vector< vector<Integer> > >::const_iterator it=multi_input_data.begin();
    // find specific generator type -- there is only one, as checked already

    normalization=false;

    Generators=Matrix<Integer>(0,dim);
    for(; it != multi_input_data.end(); ++it) {
        switch (it->first) {
            case Type::normalization:
            case Type::cone_and_lattice:
                normalization=true;
                LatticeGenerators.append(it->second);
            case Type::vertices:
            case Type::polyhedron:
            case Type::cone:
            case Type::integral_closure:
                Generators.append(it->second);
                break;
            case Type::polytope:
                Generators.append(prepare_input_type_2(it->second));
                break;
            case Type::rees_algebra:
                Generators.append(prepare_input_type_3(it->second));
                break;
            case Type::lattice:
                LatticeGenerators.append(it->second);
                break;
            case Type::saturation:
                LatticeGenerators.append(it->second);
                LatticeGenerators.saturate();
                break;
            case Type::offset:
                if(it->second.size()>1){
                  errorOutput() << "Only one offset allowed!" << endl;
                  throw BadInputException();
                }
                LatticeGenerators.append(it->second);
                break;
            default: break;
        }
    }

    if(exists_element(multi_input_data,Type::dehomogenization)){
        vector<Integer> test=Generators.MxV(Dehomogenization);
        for(size_t i=0;i<test.size();++i)
            if(test[i]<0){
                errorOutput() << "Dehomogenization has has negative value on generator " << Generators[i];
                throw BadInputException();
            }
    }
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::process_lattice_data(const Matrix<Integer>& LatticeGenerators, Matrix<Integer>& Congruences, Matrix<Integer>& Equations) {

    if(!BC_set)
        compose_basis_change(Sublattice_Representation<Integer>(dim));

    bool no_constraints=(Congruences.nr_of_rows()==0) && (Equations.nr_of_rows()==0);
    bool only_cone_gen=(Generators.nr_of_rows()!=0) && no_constraints && (LatticeGenerators.nr_of_rows()==0);

    no_lattice_restriction=true;

    if(only_cone_gen){
        Sublattice_Representation<Integer> Basis_Change(Generators,true);
        compose_basis_change(Basis_Change);
        return;
    }

    if(normalization && no_constraints){
        Sublattice_Representation<Integer> Basis_Change(Generators,false);
        compose_basis_change(Basis_Change);
        return;
    }

    no_lattice_restriction=false;

    if(Generators.nr_of_rows()!=0){
        Equations.append(Generators.kernel());
    }

    if(LatticeGenerators.nr_of_rows()!=0){
        Sublattice_Representation<Integer> GenSublattice(LatticeGenerators,false);
        if((Equations.nr_of_rows()==0) && (Congruences.nr_of_rows()==0)){
            compose_basis_change(GenSublattice);
            return;
        }
        Congruences.append(GenSublattice.getCongruencesMatrix());
        Equations.append(GenSublattice.getEquationsMatrix());
    }

    if (Congruences.nr_of_rows() > 0) {
        bool zero_modulus;
        Matrix<Integer> Ker_Basis=Congruences.solve_congruences(zero_modulus);
        if(zero_modulus) {
            errorOutput() << "Modulus 0 in congruence!" << endl;
            throw BadInputException();
        }
        Sublattice_Representation<Integer> Basis_Change(Ker_Basis,false);
        compose_basis_change(Basis_Change);
    }

    if (Equations.nr_of_rows()>0) {
        Matrix<Integer> Ker_Basis=BasisChange.to_sublattice_dual(Equations).kernel();
        Sublattice_Representation<Integer> Basis_Change(Ker_Basis,true);
        compose_basis_change(Basis_Change);
    }
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::prepare_input_type_4(Matrix<Integer>& Inequalities) {

    if(inhomogeneous){
        SupportHyperplanes=Matrix<Integer>(1,dim);  // insert truncation as first inequality
        SupportHyperplanes[0]=Dehomogenization;
    }
    else
        SupportHyperplanes=Matrix<Integer>(0,dim); // here we start from the empty matrix

    if (Inequalities.nr_of_rows() == 0) {
        if (verbose) {
            verboseOutput() << "No inequalities specified in constraint mode, using non-negative orthant." << endl;
        }
        if(inhomogeneous){
            vector<Integer> test(dim);
            test[dim-1]=1;
            size_t matsize=dim;
            if(test==Dehomogenization) // in this case "last coordinate >= 0" is already there
                matsize=dim-1;   // we don't check for any other coincidence
            Inequalities= Matrix<Integer>(matsize,dim);
            for(size_t j=0;j<matsize;++j)
                Inequalities[j][j]=1;
        }
        else
            Inequalities = Matrix<Integer>(dim);
    }

    SupportHyperplanes.append(Inequalities);  // now the (remaining) inequalities are inserted
}


//---------------------------------------------------------------------------

/* polytope input */
template<typename Integer>
Matrix<Integer> Cone<Integer>::prepare_input_type_2(const vector< vector<Integer> >& Input) {
    size_t j;
    size_t nr = Input.size();
    //append a column of 1
    Matrix<Integer> Generators(nr, dim);
    for (size_t i=0; i<nr; i++) {
        for (j=0; j<dim-1; j++)
            Generators[i][j] = Input[i][j];
        Generators[i][dim-1]=1;
    }
    // use the added last component as grading
    Grading = vector<Integer>(dim,0);
    Grading[dim-1] = 1;
    is_Computed.set(ConeProperty::Grading);
    return Generators;
}

//---------------------------------------------------------------------------

/* rees input */
template<typename Integer>
Matrix<Integer> Cone<Integer>::prepare_input_type_3(const vector< vector<Integer> >& InputV) {
    Matrix<Integer> Input(InputV);
    int i,j,k,nr_rows=Input.nr_of_rows(), nr_columns=Input.nr_of_columns();
    rees_primary=true;
    // Integer number;
    Matrix<Integer> Full_Cone_Generators(nr_rows+nr_columns,nr_columns+1,0);
    for (i = 0; i < nr_columns; i++) {
        Full_Cone_Generators[i][i]=1;
    }
    for(i=0; i<nr_rows; i++){
        Full_Cone_Generators[i+nr_columns][nr_columns]=1;
        for(j=0; j<nr_columns; j++) {
            Full_Cone_Generators[i+nr_columns][j]=Input[i][j];
        }
    }
    vector<bool>  Prim_Test(nr_columns,false);
    for(i=0; i<nr_rows; i++){           //preparing the matrix for primarity test
        k=0;
        size_t v=0;
        for(j=0; j<nr_columns; j++)
            if (Input[i][j]!=0 ){
                    k++;
                    v=j;
            }
        if(k==1)
            Prim_Test[v]=true;
    }
    rees_primary=true;
    for(i=0; i<nr_columns; i++)
        if(!Prim_Test[i])
            rees_primary=false;

    is_Computed.set(ConeProperty::IsReesPrimary);
    return Full_Cone_Generators;
}


//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::prepare_input_lattice_ideal(map< InputType, vector< vector<Integer> > >& multi_input_data) {

    Matrix<Integer> Binomials(find_input_matrix(multi_input_data,Type::lattice_ideal));

    if (isComputed(ConeProperty::Grading)) {
        //check if binomials are homogeneous
        vector<Integer> degrees = Binomials.MxV(Grading);
        for (size_t i=0; i<degrees.size(); ++i) {
            if (degrees[i]!=0) {
                errorOutput() << "Grading gives non-zero value " << degrees[i]
                              << " for binomial " << i+1 << "!" << endl;
                throw BadInputException();
            }
            if (Grading[i] <= 0) {
                errorOutput() << "Grading gives non-positive value " << Grading[i]
                            << " for generator " << i+1 << "!" << endl;
                throw BadInputException();
            }
        }
    }

    Matrix<Integer> Gens=Binomials.kernel().transpose();
    Full_Cone<Integer> FC(Gens);
    FC.verbose=verbose;
    if (verbose) verboseOutput() << "Computing a positive embedding..." << endl;

    FC.dualize_cone();
    Matrix<Integer> Supp_Hyp=FC.getSupportHyperplanes().sort_lex();
    Matrix<Integer> Selected_Supp_Hyp_Trans=(Supp_Hyp.submatrix(Supp_Hyp.max_rank_submatrix_lex())).transpose();
    Matrix<Integer> Positive_Embedded_Generators=Gens.multiplication(Selected_Supp_Hyp_Trans);
    // GeneratorsOfToricRing = Positive_Embedded_Generators;
    // is_Computed.set(ConeProperty::GeneratorsOfToricRing);
    dim = Positive_Embedded_Generators.nr_of_columns();
    multi_input_data.insert(make_pair(Type::normalization,Positive_Embedded_Generators.get_elements())); // this is the cone defined by the binomials

    if (isComputed(ConeProperty::Grading)) {
        // solve GeneratorsOfToricRing * grading = old_grading
        Integer dummyDenom;
        // Grading must be set directly since map entry has been processed already
        Grading = Positive_Embedded_Generators.solve_rectangular(Grading,dummyDenom);
        if (Grading.size() != dim) {
            errorOutput() << "Grading could not be transferred!"<<endl;
            is_Computed.set(ConeProperty::Grading, false);
        }
    }
}

/* only used by the constructors */
template<typename Integer>
void Cone<Integer>::initialize() {
    BC_set=false;
    is_Computed = bitset<ConeProperty::EnumSize>();  //initialized to false
    dim = 0;
    inhomogeneous=false;
    rees_primary = false;
    triangulation_is_nested = false;
    triangulation_is_partial = false;
    verbose = libnormaliz::verbose; //take the global default
    if (using_GMP<Integer>()) {
        change_integer_type = true;
    } else {
        change_integer_type = false;
    }
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::compose_basis_change(const Sublattice_Representation<Integer>& BC) {
    if (BC_set) {
        BasisChange.compose(BC);
    } else {
        BasisChange = BC;
        BC_set = true;
    }
}
//---------------------------------------------------------------------------
template<typename Integer>
void Cone<Integer>::check_precomputed_support_hyperplanes(){

    if (isComputed(ConeProperty::Generators)) {
        // check if the inequalities are at least valid
        // if (PreComputedSupportHyperplanes.nr_of_rows() != 0) {
            Integer sp;
            for (size_t i = 0; i < Generators.nr_of_rows(); ++i) {
                for (size_t j = 0; j < PreComputedSupportHyperplanes.nr_of_rows(); ++j) {
                    if ((sp = v_scalar_product(Generators[i], PreComputedSupportHyperplanes[j])) < 0) {
                        errorOutput() << "Precomputed nequality " << j
                        << " is not valid for generator " << i
                        << " (value " << sp << ")" << endl;
                        throw BadInputException();
                    }
                }
            }
        // }
    }
}

//---------------------------------------------------------------------------
template<typename Integer>
void Cone<Integer>::check_excluded_faces(){

    if (isComputed(ConeProperty::Generators)) {
        // check if the inequalities are at least valid
        // if (ExcludedFaces.nr_of_rows() != 0) {
            Integer sp;
            for (size_t i = 0; i < Generators.nr_of_rows(); ++i) {
                for (size_t j = 0; j < ExcludedFaces.nr_of_rows(); ++j) {
                    if ((sp = v_scalar_product(Generators[i], ExcludedFaces[j])) < 0) {
                        errorOutput() << "Excluded face " << j
                        << " is not valid for generator " << i
                        << " (value " << sp << ")" << endl;
                        throw BadInputException();
                    }
                }
            }
        // }
    }
}


//---------------------------------------------------------------------------

template<typename Integer>
bool Cone<Integer>::setVerbose (bool v) {
    //we want to return the old value
    bool old = verbose;
    verbose = v;
    return old;
}
//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::deactivateChangeOfPrecision() {
    change_integer_type = false;
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::setGrading (const vector<Integer>& lf) {
    if (lf.size() != dim) {
        errorOutput() << "Grading linear form has wrong dimension " << lf.size()
        << " (should be " << dim << ")" << endl;
        throw BadInputException();
    }
    if (isComputed(ConeProperty::Generators) && Generators.nr_of_rows() > 0) {
        vector<Integer> degrees = Generators.MxV(lf);
        for (size_t i=0; i<degrees.size(); ++i) {
            if (degrees[i]<1 && (!inhomogeneous || Generators[i][dim-1]==0)) { // in the inhomogeneous case: test only generators of tail cone
                errorOutput() << "Grading gives non-positive value " << degrees[i]
                << " for generator " << i+1 << "!" << endl;
                throw BadInputException();
            }
        }
        // GradingDenom = degrees[0] / v_scalar_product(BasisChange.to_sublattice_dual(lf),BasisChange.to_sublattice(Generators[0])); //TODO in Sublattice Rep berechnen lassen
        vector<Integer> test_grading=BasisChange.to_sublattice_dual_no_div(lf);
        GradingDenom=v_make_prime(test_grading);
    } else {
        GradingDenom = 1;
    }
    //check if the linear forms are the same
    if (isComputed(ConeProperty::Grading) && Grading == lf) {
        return;
    }
    Grading = lf;
    is_Computed.set(ConeProperty::Grading);

    //remove data that depend on the grading
    is_Computed.reset(ConeProperty::IsDeg1ExtremeRays);
    is_Computed.reset(ConeProperty::IsDeg1HilbertBasis);
    is_Computed.reset(ConeProperty::Deg1Elements);
    Deg1Elements = Matrix<Integer>(0,dim);
    is_Computed.reset(ConeProperty::HilbertSeries);
    is_Computed.reset(ConeProperty::Multiplicity);

}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::setDehomogenization (const vector<Integer>& lf) {
    if (lf.size() != dim) {
        errorOutput() << "Dehomogenizing linear form has wrong dimension " << lf.size()
        << " (should be " << dim << ")" << endl;
        throw BadInputException();
    }
    Dehomogenization=lf;
    is_Computed.set(ConeProperty::Dehomogenization);
}

//---------------------------------------------------------------------------

/* check what is computed */
template<typename Integer>
bool Cone<Integer>::isComputed(ConeProperty::Enum prop) const {
    return is_Computed.test(prop);
}

template<typename Integer>
bool Cone<Integer>::isComputed(ConeProperties CheckComputed) const {
    return CheckComputed.reset(is_Computed).any();
}


/* getter */
template<typename Integer>
size_t Cone<Integer>::getRank() {
    compute(ConeProperty::Sublattice);
    return BasisChange.getRank();
}

template<typename Integer>    // computation depends on OriginalMonoidGenerators
Integer Cone<Integer>::getIndex() {
    compute(ConeProperty::OriginalMonoidGenerators);
    return index;
}

template<typename Integer>
size_t Cone<Integer>::getRecessionRank() {
    compute(ConeProperty::RecessionRank);
    return recession_rank;
}

template<typename Integer>
long Cone<Integer>::getAffineDim() {
    compute(ConeProperty::AffineDim);
    return affine_dim;
}

template<typename Integer>
const Sublattice_Representation<Integer>& Cone<Integer>::getSublattice() {
    compute(ConeProperty::Sublattice);
    return BasisChange;
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getOriginalMonoidGeneratorsMatrix() {
    compute(ConeProperty::OriginalMonoidGenerators);
    return OriginalMonoidGenerators;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getOriginalMonoidGenerators() {
    compute(ConeProperty::OriginalMonoidGenerators);
    return OriginalMonoidGenerators.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrOriginalMonoidGenerators() {
    compute(ConeProperty::OriginalMonoidGenerators);
    return OriginalMonoidGenerators.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getGeneratorsMatrix() {
    compute(ConeProperty::Generators);
    return Generators;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getGenerators() {
    compute(ConeProperty::Generators);
    return Generators.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrGenerators() {
    compute(ConeProperty::Generators);
    return Generators.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getExtremeRaysMatrix() {
    compute(ConeProperty::ExtremeRays);
    return ExtremeRays;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getExtremeRays() {
    compute(ConeProperty::ExtremeRays);
    return ExtremeRays.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrExtremeRays() {
    compute(ConeProperty::ExtremeRays);
    return ExtremeRays.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getVerticesOfPolyhedronMatrix() {
    compute(ConeProperty::VerticesOfPolyhedron);
    return VerticesOfPolyhedron;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getVerticesOfPolyhedron() {
    compute(ConeProperty::VerticesOfPolyhedron);
    return VerticesOfPolyhedron.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrVerticesOfPolyhedron() {
    compute(ConeProperty::VerticesOfPolyhedron);
    return VerticesOfPolyhedron.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getSupportHyperplanesMatrix() {
    compute(ConeProperty::SupportHyperplanes);
    return SupportHyperplanes;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getSupportHyperplanes() {
    compute(ConeProperty::SupportHyperplanes);
    return SupportHyperplanes.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrSupportHyperplanes() {
    compute(ConeProperty::SupportHyperplanes);
    return SupportHyperplanes.nr_of_rows();
}

template<typename Integer>
map< InputType , vector< vector<Integer> > > Cone<Integer>::getConstraints () {
    compute(ConeProperty::Sublattice, ConeProperty::SupportHyperplanes);
    map<InputType, vector< vector<Integer> > > c;
    c[Type::inequalities] = SupportHyperplanes.get_elements();
    c[Type::equations] = BasisChange.getEquations();
    c[Type::congruences] = BasisChange.getCongruences();
    return c;
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getExcludedFacesMatrix() {
    compute(ConeProperty::ExcludedFaces);
    return ExcludedFaces;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getExcludedFaces() {
    compute(ConeProperty::ExcludedFaces);
    return ExcludedFaces.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrExcludedFaces() {
    compute(ConeProperty::ExcludedFaces);
    return ExcludedFaces.nr_of_rows();
}

template<typename Integer>
const vector< pair<vector<key_t>,Integer> >& Cone<Integer>::getTriangulation() {
    compute(ConeProperty::Triangulation);
    return Triangulation;
}

template<typename Integer>
const vector< pair<vector<key_t>,long> >& Cone<Integer>::getInclusionExclusionData() {
    compute(ConeProperty::InclusionExclusionData);
    return InExData;
}

template<typename Integer>
const list< STANLEYDATA<Integer> >& Cone<Integer>::getStanleyDec() {
    compute(ConeProperty::StanleyDec);
    return StanleyDec;
}

template<typename Integer>
size_t Cone<Integer>::getTriangulationSize() {
    compute(ConeProperty::TriangulationSize);
    return TriangulationSize;
}

template<typename Integer>
Integer Cone<Integer>::getTriangulationDetSum() {
    compute(ConeProperty::TriangulationDetSum);
    return TriangulationDetSum;
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getHilbertBasisMatrix() {
    compute(ConeProperty::HilbertBasis);
    return HilbertBasis;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getHilbertBasis() {
    compute(ConeProperty::HilbertBasis);
    return HilbertBasis.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrHilbertBasis() {
    compute(ConeProperty::HilbertBasis);
    return HilbertBasis.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getModuleGeneratorsOverOriginalMonoidMatrix() {
    compute(ConeProperty::ModuleGeneratorsOverOriginalMonoid);
    return ModuleGeneratorsOverOriginalMonoid;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getModuleGeneratorsOverOriginalMonoid() {
    compute(ConeProperty::ModuleGeneratorsOverOriginalMonoid);
    return ModuleGeneratorsOverOriginalMonoid.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrModuleGeneratorsOverOriginalMonoid() {
    compute(ConeProperty::ModuleGeneratorsOverOriginalMonoid);
    return ModuleGeneratorsOverOriginalMonoid.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getModuleGeneratorsMatrix() {
    compute(ConeProperty::ModuleGenerators);
    return ModuleGenerators;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getModuleGenerators() {
    compute(ConeProperty::ModuleGenerators);
    return ModuleGenerators.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrModuleGenerators() {
    compute(ConeProperty::ModuleGenerators);
    return ModuleGenerators.nr_of_rows();
}

template<typename Integer>
const Matrix<Integer>& Cone<Integer>::getDeg1ElementsMatrix() {
    compute(ConeProperty::Deg1Elements);
    return Deg1Elements;
}
template<typename Integer>
const vector< vector<Integer> >& Cone<Integer>::getDeg1Elements() {
    compute(ConeProperty::Deg1Elements);
    return Deg1Elements.get_elements();
}
template<typename Integer>
size_t Cone<Integer>::getNrDeg1Elements() {
    compute(ConeProperty::Deg1Elements);
    return Deg1Elements.nr_of_rows();
}

template<typename Integer>
const HilbertSeries& Cone<Integer>::getHilbertSeries() {
    compute(ConeProperty::HilbertSeries);
    return HSeries;
}

template<typename Integer>
vector<Integer> Cone<Integer>::getGrading() {
    compute(ConeProperty::Grading);
    return Grading;
}

template<typename Integer>
Integer Cone<Integer>::getGradingDenom() {
    compute(ConeProperty::Grading);
    return GradingDenom;
}

template<typename Integer>
vector<Integer> Cone<Integer>::getDehomogenization() {
    compute(ConeProperty::Dehomogenization);
    return Dehomogenization;
}

template<typename Integer>
mpq_class Cone<Integer>::getMultiplicity() {
    compute(ConeProperty::Multiplicity);
    return multiplicity;
}

template<typename Integer>
bool Cone<Integer>::isPointed() {
    compute(ConeProperty::IsPointed);
    return pointed;
}

template<typename Integer>
bool Cone<Integer>::isInhomogeneous() {
    return inhomogeneous;
}

template<typename Integer>
bool Cone<Integer>::isDeg1ExtremeRays() {
    compute(ConeProperty::IsDeg1ExtremeRays);
    return deg1_extreme_rays;
}

template<typename Integer>
bool Cone<Integer>::isDeg1HilbertBasis() {
    compute(ConeProperty::IsDeg1HilbertBasis);
    return deg1_hilbert_basis;
}

template<typename Integer>
bool Cone<Integer>::isIntegrallyClosed() {
    compute(ConeProperty::IsIntegrallyClosed);
    return integrally_closed;
}

template<typename Integer>
bool Cone<Integer>::isReesPrimary() {
    compute(ConeProperty::IsReesPrimary);
    return rees_primary;
}

template<typename Integer>
Integer Cone<Integer>::getReesPrimaryMultiplicity() {
    compute(ConeProperty::ReesPrimaryMultiplicity);
    return ReesPrimaryMultiplicity;
}

// the information about the triangulation will just be returned
// if no triangulation was computed so far they return false
template<typename Integer>
bool Cone<Integer>::isTriangulationNested() {
    return triangulation_is_nested;
}
template<typename Integer>
bool Cone<Integer>::isTriangulationPartial() {
    return triangulation_is_partial;
}

template<typename Integer>
size_t Cone<Integer>::getModuleRank() {
    compute(ConeProperty::ModuleRank);
    return module_rank;
}

template<typename Integer>
vector<Integer> Cone<Integer>::getClassGroup() {
    compute(ConeProperty::ClassGroup);
    return ClassGroup;
}


//---------------------------------------------------------------------------

template<typename Integer>
ConeProperties Cone<Integer>::compute(ConeProperty::Enum cp) {
    if (isComputed(cp)) return ConeProperties();
    return compute(ConeProperties(cp));
}

template<typename Integer>
ConeProperties Cone<Integer>::compute(ConeProperty::Enum cp1, ConeProperty::Enum cp2) {
    return compute(ConeProperties(cp1,cp2));
}

template<typename Integer>
ConeProperties Cone<Integer>::compute(ConeProperty::Enum cp1, ConeProperty::Enum cp2,
                                      ConeProperty::Enum cp3) {
    return compute(ConeProperties(cp1,cp2,cp3));
}

//---------------------------------------------------------------------------

template<typename Integer>
ConeProperties Cone<Integer>::compute(ConeProperties ToCompute) {

    // handle zero cone as special case, makes our life easier
    if (BasisChange.getRank() == 0) {
        set_zero_cone();
        ToCompute.reset(is_Computed);
        return ToCompute;
    }

    ToCompute.set_preconditions();
    ToCompute.prepare_compute_options();
    ToCompute.check_sanity(inhomogeneous);
    if(ToCompute.test(ConeProperty::ModuleGeneratorsOverOriginalMonoid) && !isComputed(ConeProperty::OriginalMonoidGenerators)){
        errorOutput() << "ERROR: Module generators over original monoid only computable if original monoid is defined!"
                << endl;
        throw BadInputException();
    }


    if (ToCompute.test(ConeProperty::DualMode)) {
        compute_dual(ToCompute);
    }
    ToCompute.reset(is_Computed);
    if (ToCompute.none()){
        return ToCompute;
    }

    /* preparation: get generators if necessary */
    compute_generators();
    is_Computed.set(ConeProperty::Sublattice); // will not be changed anymore
    if (BasisChange.getRank() == 0) {
        set_zero_cone();
        ToCompute.reset(is_Computed);
        return ToCompute;
    }
    if (!isComputed(ConeProperty::Generators)) {
        errorOutput()<<"FATAL ERROR: Could not get Generators. This should not happen!"<<endl;
        throw FatalException();
    }


    ToCompute.reset(is_Computed); // already computed
    if (ToCompute.none()) {
        return ToCompute;
    }

    /* if (rees_primary) // && ToCompute.test(ConeProperty::ReesPrimaryMultiplicity))
        ToCompute.set(ConeProperty::Triangulation); */

    // the actual computation
    if (change_integer_type) {
        try {
            compute_inner<MachineInteger>(ToCompute);
        } catch(const ArithmeticException& ) {
            errorOutput() << "ArithmeticException caught. Restart with a bigger type." << endl;
            change_integer_type = false;
        }
    }
    if (!change_integer_type) {
        compute_inner<Integer>(ToCompute);
    }

    /* check if everything is computed */
    ToCompute.reset(is_Computed); //remove what is now computed
    ToCompute.reset_compute_options();
    if (!ToCompute.test(ConeProperty::DefaultMode) && ToCompute.any()) {
        errorOutput() << "ERROR: Cone could not compute everything that was asked for!"<<endl;
        errorOutput() << "Missing: " << ToCompute << endl;
        throw NotComputableException(ToCompute);
    }
    ToCompute.reset(ConeProperty::DefaultMode);
    return ToCompute;
}

template<typename Integer>
template<typename IntegerFC>
void Cone<Integer>::compute_inner(ConeProperties& ToCompute) {
    Matrix<IntegerFC> FC_Gens;
    BasisChange.convert_to_sublattice(FC_Gens, Generators);
    Full_Cone<IntegerFC> FC(FC_Gens,!ToCompute.test(ConeProperty::ModuleGeneratorsOverOriginalMonoid));
    // !ToCompute.test(ConeProperty::ModuleGeneratorsOverOriginalMonoid) blocks make_prime in full_cone.cpp

    /* activate bools in FC */

    FC.verbose=verbose;

    FC.inhomogeneous=inhomogeneous;

    if (ToCompute.test(ConeProperty::HilbertSeries)) {
        FC.do_h_vector = true;
    }
    if (ToCompute.test(ConeProperty::HilbertBasis)) {
        FC.do_Hilbert_basis = true;
    }
    if (ToCompute.test(ConeProperty::Triangulation)) {
        FC.keep_triangulation = true;
    }
    if (ToCompute.test(ConeProperty::Multiplicity) ) {
        FC.do_multiplicity = true;
    }
    if (ToCompute.test(ConeProperty::TriangulationDetSum) ) {
        FC.do_determinants = true;
    }
    if (ToCompute.test(ConeProperty::TriangulationSize)) {
        FC.do_triangulation = true;
    }
    if (ToCompute.test(ConeProperty::Deg1Elements)) {
        FC.do_deg1_elements = true;
    }
    if (ToCompute.test(ConeProperty::StanleyDec)) {
        FC.do_Stanley_dec = true;
    }
    if (ToCompute.test(ConeProperty::Approximate)
     && ToCompute.test(ConeProperty::Deg1Elements)) {
        FC.do_approximation = true;
        FC.do_deg1_elements = true;
    }
    if (ToCompute.test(ConeProperty::DefaultMode)) {
        FC.do_default_mode = true;
    }
    if (ToCompute.test(ConeProperty::BottomDecomposition)) {
        FC.do_bottom_dec = true;
    }
    if (ToCompute.test(ConeProperty::KeepOrder)) {
        FC.keep_order = true;
    }
    if (ToCompute.test(ConeProperty::ClassGroup)) {
        FC.do_class_group=true;
    }
    /* Give extra data to FC */
    if ( isComputed(ConeProperty::ExtremeRays) ) {
        FC.Extreme_Rays = ExtremeRaysIndicator;
        FC.is_Computed.set(ConeProperty::ExtremeRays);
    }
    if (ExcludedFaces.nr_of_rows()!=0) {
        BasisChange.convert_to_sublattice_dual(FC.ExcludedFaces, ExcludedFaces);
    }

    if (inhomogeneous){
        BasisChange.convert_to_sublattice_dual_no_div(FC.Truncation, Dehomogenization);
    }
    if ( isComputed(ConeProperty::Grading) ) {  // IMPORTANT: Truncation must be set before Grading
        BasisChange.convert_to_sublattice_dual(FC.Grading, Grading);
        FC.is_Computed.set(ConeProperty::Grading);
        if (inhomogeneous)
            FC.find_grading_inhom();
        FC.set_degrees();
    }

    if (SupportHyperplanes.nr_of_rows()!=0) {
         BasisChange.convert_to_sublattice_dual(FC.Support_Hyperplanes, SupportHyperplanes);
    }
    if (isComputed(ConeProperty::SupportHyperplanes)){
        FC.is_Computed.set(ConeProperty::SupportHyperplanes);
        FC.do_all_hyperplanes = false;
    }

    if(ToCompute.test(ConeProperty::ModuleGeneratorsOverOriginalMonoid)){
        FC.do_module_gens_intcl=true;
    }

    /* do the computation */
    FC.compute();

    extract_data(FC);
}


template<typename Integer>
void Cone<Integer>::compute_generators() {
    //create Generators from SupportHyperplanes
    if (!isComputed(ConeProperty::Generators) && SupportHyperplanes.nr_of_rows()!=0) {
        if (verbose) {
            verboseOutput() << "Computing extreme rays as support hyperplanes of the dual cone:" << endl;
        }
        if (change_integer_type) {
            try {
                compute_generators_inner<MachineInteger>();
            } catch(const ArithmeticException& ) {
                errorOutput() << "ArithmeticException caught. Restart with a bigger type." << endl;
                change_integer_type = false;
            }
        }
        if (!change_integer_type) {
            compute_generators_inner<Integer>();
        }
    }
    assert(isComputed(ConeProperty::Generators));
}

template<typename Integer>
template<typename IntegerFC>
void Cone<Integer>::compute_generators_inner() {
    Matrix<IntegerFC> Dual_Gen;
    BasisChange.convert_to_sublattice_dual(Dual_Gen, SupportHyperplanes);
    Full_Cone<IntegerFC> Dual_Cone(Dual_Gen);
    Dual_Cone.verbose=verbose;
    Dual_Cone.do_extreme_rays=true; // we try to find them, need not exist
    Dual_Cone.dualize_cone();
    if (Dual_Cone.isComputed(ConeProperty::SupportHyperplanes)) {
        //get the extreme rays of the primal cone
        Matrix<Integer> Extreme_Rays;
        convert(Extreme_Rays, Dual_Cone.getSupportHyperplanes());
        Generators = BasisChange.from_sublattice(Extreme_Rays);
        is_Computed.set(ConeProperty::Generators);
        set_extreme_rays(vector<bool>(Generators.nr_of_rows(),true));
        if (Dual_Cone.isComputed(ConeProperty::ExtremeRays)) {
            //get minmal set of support_hyperplanes
            Matrix<IntegerFC> Supp_Hyp = Dual_Cone.getGenerators().submatrix(Dual_Cone.getExtremeRays());
            BasisChange.convert_from_sublattice_dual(SupportHyperplanes, Supp_Hyp);
            is_Computed.set(ConeProperty::SupportHyperplanes);
        }
        Sublattice_Representation<Integer> Basis_Change(Extreme_Rays,true);
        compose_basis_change(Basis_Change);

        // check grading and compute denominator
        if (isComputed(ConeProperty::Grading) && Generators.nr_of_rows() > 0) {
            setGrading(Grading);
        }
        // compute grading, so that it is also known if nothing else is done afterwards
        if (!isComputed(ConeProperty::Grading) && !inhomogeneous) {
            // Generators = ExtremeRays
            vector<Integer> lf = BasisChange.to_sublattice(Generators).find_linear_form();
            if (lf.size() == BasisChange.getRank()) {
                vector<Integer> test_lf=BasisChange.from_sublattice_dual(lf);
                if(Generators.nr_of_rows()==0 || v_scalar_product(Generators[0],test_lf)==1)
                    setGrading(test_lf);
            }
        }
    }
}


template<typename Integer>
void Cone<Integer>::compute_dual(ConeProperties& ToCompute) {

    ToCompute.reset(is_Computed);
    if (ToCompute.none() || !( ToCompute.test(ConeProperty::Deg1Elements)
                            || ToCompute.test(ConeProperty::HilbertBasis))) {
        return;
    }

    if (change_integer_type) {
        try {
            compute_dual_inner<MachineInteger>(ToCompute);
        } catch(const ArithmeticException& ) {
            errorOutput() << "ArithmeticException caught. Restart with a bigger type." << endl;
            change_integer_type = false;
        }
    }
    if (!change_integer_type) {
        compute_dual_inner<Integer>(ToCompute);
    }
    ToCompute.reset(ConeProperty::DualMode);
    ToCompute.reset(is_Computed);
}

template<typename Integer>
template<typename IntegerFC>
void Cone<Integer>::compute_dual_inner(ConeProperties& ToCompute) {

    bool do_only_Deg1_Elements = ToCompute.test(ConeProperty::Deg1Elements)
                                 && !ToCompute.test(ConeProperty::HilbertBasis);

    if(isComputed(ConeProperty::Generators) && SupportHyperplanes.nr_of_rows()==0){
        if (verbose) {
            verboseOutput()<<  "Computing support hyperplanes for the dual mode:"<< endl;
        }
        Matrix<IntegerFC> Tmp_Gens;
        BasisChange.convert_to_sublattice(Tmp_Gens,Generators);
        Full_Cone<IntegerFC> Tmp_Cone(Tmp_Gens);
        Tmp_Cone.verbose=verbose;
        /* if (ToCompute.test(ConeProperty::KeepOrder)) {
            Tmp_Cone.keep_order = true;
            Tmp_Cone.is_Computed.set(ConeProperty::KeepOrder);
        }*/
        Tmp_Cone.do_extreme_rays=true;
        Tmp_Cone.dualize_cone();        // also marks extreme rays
        extract_data(Tmp_Cone);
        if(inhomogeneous){
            Matrix<Integer> Help(SupportHyperplanes.nr_of_rows()+1,dim);  // make Dehomogenization the first inequality
            Help[0]=Dehomogenization;
            Help.append(SupportHyperplanes);
            SupportHyperplanes=Help;
        }
    }

    if((do_only_Deg1_Elements || inhomogeneous) && !isComputed(ConeProperty::ExtremeRays)){
        if (verbose) {
            verboseOutput() << "Computing extreme rays for the dual mode:"<< endl;
        }
        Matrix<Integer> Help(0,dim);
        if(inhomogeneous)                        // we must guard ourselves against loosing the truncation
            Help=SupportHyperplanes;
        compute_generators();   // computes extreme rays, but does not find grading !
        if(inhomogeneous)                        // we must guard ourselves against loosing the truncation
            SupportHyperplanes=Help;
        if (BasisChange.getRank() == 0) {
            set_zero_cone();
            ToCompute.reset(is_Computed);
            return;
        }
    }

    if(do_only_Deg1_Elements && !isComputed(ConeProperty::Grading)){
        vector<Integer> lf= Generators.submatrix(ExtremeRaysIndicator).find_linear_form_low_dim();
        if(Generators.nr_of_rows()==0 || (lf.size()==dim && v_scalar_product(Generators[0],lf)==1))
            setGrading(lf);
        else{
            errorOutput() << "Need grading to compute degree 1 elements and cannot find one." << endl;
            throw BadInputException();
        }
    }

    if (SupportHyperplanes.nr_of_rows()==0) {
        errorOutput()<<"FATAL ERROR: Could not get SupportHyperplanes. This should not happen!"<<endl;
        throw FatalException();
    }

    size_t i,j;
    Matrix<IntegerFC> Inequ_on_Ker;
    BasisChange.convert_to_sublattice_dual(Inequ_on_Ker,SupportHyperplanes);
    size_t newdim = Inequ_on_Ker.nr_of_columns();
    //now sort the inequalities, hopefully this makes the computation faster
    IntegerFC norm;
    vector< IntegerFC > hyperplane;
    multimap <IntegerFC , vector <IntegerFC> >  SortingHelp;
    typename multimap <IntegerFC , vector <IntegerFC> >::const_iterator ii;

    size_t i_start=0;
    if (inhomogeneous) {
        // in the inhomogeneous case the truncation will be (re)inserted below
        i_start=1;
        vector< IntegerFC > help;
        BasisChange.convert_to_sublattice_dual(help, Dehomogenization);
        if(Inequ_on_Ker[0] != help)
            i_start=0;
    }
    for (i = i_start; i < Inequ_on_Ker.nr_of_rows() ; i++) {
        hyperplane=Inequ_on_Ker[i];
        norm=0;
        for (j = 0; j <newdim; j++) {
            norm+=Iabs(hyperplane[j]);
        }
        SortingHelp.insert(make_pair(norm,hyperplane));
    }
    size_t inhom_corr=0;
    if(inhomogeneous || do_only_Deg1_Elements)
        inhom_corr=1;
    Matrix<IntegerFC> Inequ_Ordered(Inequ_on_Ker.nr_of_rows()+inhom_corr,newdim);
    if (inhomogeneous) {
        // insert truncation as the first inequality
        BasisChange.convert_to_sublattice_dual_no_div(Inequ_Ordered[0], Dehomogenization);
    }
    if (do_only_Deg1_Elements) {
        // in this case the grading acts as truncation and it is a NEW inequality
        BasisChange.convert_to_sublattice_dual(Inequ_Ordered[0], Grading);
    }
    i=inhom_corr;
    for (ii=SortingHelp.begin(); ii != SortingHelp.end(); ii++) {
        Inequ_Ordered[i]=(*ii).second;
        i++;
    }

    Cone_Dual_Mode<IntegerFC> ConeDM(Inequ_Ordered);
    ConeDM.verbose=verbose;
    ConeDM.inhomogeneous=inhomogeneous;
    ConeDM.do_only_Deg1_Elements=do_only_Deg1_Elements;
    if(isComputed(ConeProperty::Generators))
        BasisChange.convert_to_sublattice(ConeDM.Generators, Generators);
    if(isComputed(ConeProperty::ExtremeRays))
        ConeDM.ExtremeRays=ExtremeRaysIndicator;
    ConeDM.hilbert_basis_dual();

    // check if the rank of the sublattice has changed
    if ( ConeDM.Generators.rank() < ConeDM.dim ) {
        Sublattice_Representation<IntegerFC> SR_(ConeDM.Generators,true);
        Sublattice_Representation<Integer> SR(convertTo<Matrix<Integer>>(ConeDM.Generators),true); //TODO other conversion!
        ConeDM.to_sublattice(SR_);
        compose_basis_change(SR);
        // handle zero cone as special case, makes our life easier
        if (BasisChange.getRank() == 0) {
            set_zero_cone();
            ToCompute.reset(is_Computed);
            return;
        }
    }
    is_Computed.set(ConeProperty::Sublattice);
    // create a Full_Cone out of ConeDM
    Full_Cone<IntegerFC> FC(ConeDM);
    FC.verbose=verbose;
    // Give extra data to FC
    if ( isComputed(ConeProperty::Grading) ) {
        BasisChange.convert_to_sublattice_dual(FC.Grading, Grading);
        FC.is_Computed.set(ConeProperty::Grading);

        if(!inhomogeneous)
            FC.set_degrees();
    }
    if(inhomogeneous)
        BasisChange.convert_to_sublattice_dual(FC.Truncation, Dehomogenization);
    FC.do_class_group=ToCompute.test(ConeProperty::ClassGroup);
    FC.dual_mode();
    extract_data(FC);
}

//---------------------------------------------------------------------------

template<typename Integer>
Integer Cone<Integer>::compute_primary_multiplicity() {
    if (change_integer_type) {
        try {
            return compute_primary_multiplicity_inner<MachineInteger>();
        } catch(const ArithmeticException& ) {
            errorOutput() << "ArithmeticException caught. Restart with a bigger type." << endl;
            change_integer_type = false;
        }
    }
    return compute_primary_multiplicity_inner<Integer>();
}

template<typename Integer>
template<typename IntegerFC>
Integer Cone<Integer>::compute_primary_multiplicity_inner() {
    Matrix<IntegerFC> Ideal(0,dim-1);
    vector<IntegerFC> help(dim-1);
    for(size_t i=0;i<Generators.nr_of_rows();++i){ // select ideal generators
        if(Generators[i][dim-1]==1){
            for(size_t j=0;j<dim-1;++j)
                convert(help[j],Generators[i][j]);
            Ideal.append(help);
        }
    }
    Full_Cone<IntegerFC> IdCone(Ideal,false);
    IdCone.do_bottom_dec=true;
    IdCone.do_determinants=true;
    IdCone.compute();
    return convertTo<Integer>(IdCone.detSum);
}

//---------------------------------------------------------------------------

template<typename Integer>
template<typename IntegerFC>
void Cone<Integer>::extract_data(Full_Cone<IntegerFC>& FC) {
    //this function extracts ALL available data from the Full_Cone
    //even if it was in Cone already <- this may change
    //it is possible to delete the data in Full_Cone after extracting it

    if(verbose) {
        verboseOutput() << "transforming data..."<<flush;
    }

    if (FC.isComputed(ConeProperty::Grading)) {
        if (!isComputed(ConeProperty::Grading)) {
            BasisChange.convert_from_sublattice_dual(Grading, FC.getGrading());
            is_Computed.set(ConeProperty::Grading);
        }
        //compute denominator of Grading
        if(BasisChange.getRank()!=0){
            vector<Integer> test_grading = BasisChange.to_sublattice_dual_no_div(Grading);
            GradingDenom=v_make_prime(test_grading);
        }
    }

    WeightsGrad=Matrix<Integer> (0,dim);  // weight matrix for ordering
    if(isComputed(ConeProperty::Grading))
        WeightsGrad.append(Grading);
    GradAbs=vector<bool>(WeightsGrad.nr_of_rows(),false);

    if (rees_primary){
        ReesPrimaryMultiplicity = compute_primary_multiplicity();
        is_Computed.set(ConeProperty::ReesPrimaryMultiplicity);
    }

    if (FC.isComputed(ConeProperty::ModuleGeneratorsOverOriginalMonoid)) { // must prece extreme rays
        BasisChange.convert_from_sublattice(ModuleGeneratorsOverOriginalMonoid, FC.getModuleGeneratorsOverOriginalMonoid());
        ModuleGeneratorsOverOriginalMonoid.sort_by_weights(WeightsGrad,GradAbs);
        is_Computed.set(ConeProperty::ModuleGeneratorsOverOriginalMonoid);
    }

    if (FC.isComputed(ConeProperty::Generators)) {
        BasisChange.convert_from_sublattice(Generators,FC.getGenerators());
        is_Computed.set(ConeProperty::Generators);
    }
    if (FC.isComputed(ConeProperty::ExtremeRays)) {
        set_extreme_rays(FC.getExtremeRays());
    }
    if (FC.isComputed(ConeProperty::SupportHyperplanes)) {
        if (inhomogeneous) {
            // remove irrelevant support hyperplane 0 ... 0 1
            vector<IntegerFC> irr_hyp_subl;
            BasisChange.convert_to_sublattice_dual(irr_hyp_subl, Dehomogenization);
            FC.Support_Hyperplanes.remove_row(irr_hyp_subl);
        }
        BasisChange.convert_from_sublattice_dual(SupportHyperplanes, FC.getSupportHyperplanes());
        SupportHyperplanes.sort_lex();
        is_Computed.set(ConeProperty::SupportHyperplanes);
    }
    if (FC.isComputed(ConeProperty::TriangulationSize)) {
        TriangulationSize = FC.totalNrSimplices;
        triangulation_is_nested = FC.triangulation_is_nested;
        triangulation_is_partial= FC.triangulation_is_partial;
        is_Computed.set(ConeProperty::TriangulationSize);
        is_Computed.reset(ConeProperty::Triangulation);
        Triangulation.clear();
    }
    if (FC.isComputed(ConeProperty::TriangulationDetSum)) {
        convert(TriangulationDetSum, FC.detSum);
        is_Computed.set(ConeProperty::TriangulationDetSum);
    }
    if (FC.isComputed(ConeProperty::Triangulation)) {
        triangulation_is_nested = FC.triangulation_is_nested;
        triangulation_is_partial= FC.triangulation_is_partial;
        size_t tri_size = FC.Triangulation.size();
        Triangulation = vector< pair<vector<key_t>, Integer> >(tri_size);
        SHORTSIMPLEX<IntegerFC> simp;
        for (size_t i = 0; i<tri_size; ++i) {
            SHORTSIMPLEX<IntegerFC> simp;
            simp = FC.Triangulation.front();
            Triangulation[i].first.swap(simp.key);
            sort(Triangulation[i].first.begin(), Triangulation[i].first.end());
            if (FC.isComputed(ConeProperty::TriangulationDetSum))
                convert(Triangulation[i].second, simp.vol);
            else
                Triangulation[i].second = 0;
            FC.Triangulation.pop_front();
        }
        is_Computed.set(ConeProperty::Triangulation);
    }
    if (FC.isComputed(ConeProperty::StanleyDec)) {
        StanleyDec.clear();
        //StanleyDec.splice(StanleyDec.end(),FC.StanleyDec);
        while (!FC.StanleyDec.empty()) {
            STANLEYDATA<Integer> ele;
            ele.key.swap(FC.StanleyDec.front().key);
            convert(ele.offsets, FC.StanleyDec.front().offsets);
            StanleyDec.push_back(ele);
            FC.StanleyDec.pop_front();
        }
        is_Computed.set(ConeProperty::StanleyDec);
    }
    if (FC.isComputed(ConeProperty::InclusionExclusionData)) {
        InExData.clear();
        InExData.reserve(FC.InExCollect.size());
        map<boost::dynamic_bitset<>, long>::iterator F;
        vector<key_t> key;
        for (F=FC.InExCollect.begin(); F!=FC.InExCollect.end(); ++F) {
            key.clear();
            for (size_t i=0;i<FC.nr_gen;++i) {
                if (F->first.test(i)) {
                    key.push_back(i+1);
                }
            }
            InExData.push_back(make_pair(key,F->second));
        }
        is_Computed.set(ConeProperty::InclusionExclusionData);
    }
    if (FC.isComputed(ConeProperty::RecessionRank)) {
        recession_rank = FC.level0_dim;
        is_Computed.set(ConeProperty::RecessionRank);
        if (getRank() == recession_rank) {
            affine_dim = -1;
        } else {
            affine_dim = getRank()-1;
        }
        is_Computed.set(ConeProperty::AffineDim);
    }
    if (FC.isComputed(ConeProperty::ModuleRank)) {
        module_rank = FC.getModuleRank();
        is_Computed.set(ConeProperty::ModuleRank);
    }
    if (FC.isComputed(ConeProperty::Multiplicity)) {
        if(!inhomogeneous) {
            multiplicity = FC.getMultiplicity();
            is_Computed.set(ConeProperty::Multiplicity);
        } else if (isComputed(ConeProperty::ModuleRank)) {
            multiplicity = FC.getMultiplicity()*module_rank;
            is_Computed.set(ConeProperty::Multiplicity);
        }
    }
    if (FC.isComputed(ConeProperty::HilbertBasis)) {
        if (inhomogeneous) {
            // separate (capped) Hilbert basis to the Hilbert basis of the level 0 cone
            // and the module generators in level 1
            HilbertBasis = Matrix<Integer>(0,dim);
            ModuleGenerators = Matrix<Integer>(0,dim);
            typename list< vector<IntegerFC> >::const_iterator FCHB(FC.Hilbert_Basis.begin());
            vector<Integer> tmp;
            for (; FCHB != FC.Hilbert_Basis.end(); ++FCHB) {
                BasisChange.convert_from_sublattice(tmp,*FCHB);
                if (v_scalar_product(tmp,Dehomogenization) == 0) { // Hilbert basis element of the cone at level 0
                    HilbertBasis.append(tmp);
                } else {              // module generator
                    ModuleGenerators.append(tmp);
                }
            }
            ModuleGenerators.sort_by_weights(WeightsGrad,GradAbs);
            is_Computed.set(ConeProperty::ModuleGenerators);
        } else { // homogeneous
            BasisChange.convert_from_sublattice(HilbertBasis, FC.getHilbertBasis());
        }
        HilbertBasis.sort_by_weights(WeightsGrad,GradAbs);
        is_Computed.set(ConeProperty::HilbertBasis);
    }
    if (FC.isComputed(ConeProperty::Deg1Elements)) {
        BasisChange.convert_from_sublattice(Deg1Elements, FC.getDeg1Elements());
        Deg1Elements.sort_by_weights(WeightsGrad,GradAbs);
        is_Computed.set(ConeProperty::Deg1Elements);
    }
    if (FC.isComputed(ConeProperty::HilbertSeries)) {
        HSeries = FC.Hilbert_Series;
        is_Computed.set(ConeProperty::HilbertSeries);
    }
    if (FC.isComputed(ConeProperty::IsPointed)) {
        pointed = FC.isPointed();
        is_Computed.set(ConeProperty::IsPointed);
    }
    if (FC.isComputed(ConeProperty::IsDeg1ExtremeRays)) {
        deg1_extreme_rays = FC.isDeg1ExtremeRays();
        is_Computed.set(ConeProperty::IsDeg1ExtremeRays);
    }
    if (FC.isComputed(ConeProperty::ExcludedFaces)) {
        BasisChange.convert_from_sublattice_dual(ExcludedFaces, FC.getExcludedFaces());
        ExcludedFaces.sort_lex();
        is_Computed.set(ConeProperty::ExcludedFaces);
    }

    if (FC.isComputed(ConeProperty::IsDeg1HilbertBasis)) {
        deg1_hilbert_basis = FC.isDeg1HilbertBasis();
        is_Computed.set(ConeProperty::IsDeg1HilbertBasis);
    }
    if (FC.isComputed(ConeProperty::ClassGroup)) {
        convert(ClassGroup, FC.ClassGroup);
        is_Computed.set(ConeProperty::ClassGroup);
    }

    check_integrally_closed();

    if (verbose) {
        verboseOutput() << " done." <<endl;
    }
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::check_integrally_closed() {
    if (!isComputed(ConeProperty::OriginalMonoidGenerators) || isComputed(ConeProperty::IsIntegrallyClosed)
               || !isComputed(ConeProperty::HilbertBasis) || inhomogeneous)
        return;

    integrally_closed = false;
    long nr_gen = OriginalMonoidGenerators.nr_of_rows();
    long nr_hilb = HilbertBasis.nr_of_rows();
    if (nr_hilb <= nr_gen) {
        integrally_closed = true;
        typename list< vector<Integer> >::iterator h;
        for (long h = 0; h < nr_hilb; ++h) {
            integrally_closed = false;
            for (long i = 0; i < nr_gen; ++i) {
                if (HilbertBasis[h] == OriginalMonoidGenerators[i]) {
                    integrally_closed = true;
                    break;
                }
            }
            if (!integrally_closed) {
                break;
            }
        }
    }
    is_Computed.set(ConeProperty::IsIntegrallyClosed);
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::set_original_monoid_generators(const Matrix<Integer>& Input) {
    if (!isComputed(ConeProperty::OriginalMonoidGenerators)) {
        OriginalMonoidGenerators = Input;
        is_Computed.set(ConeProperty::OriginalMonoidGenerators);
    }
    // Generators = Input;
    // is_Computed.set(ConeProperty::Generators);
    Matrix<Integer> M=BasisChange.to_sublattice(Input);
    index=M.full_rank_index();
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::set_extreme_rays(const vector<bool>& ext) {
    assert(ext.size() == Generators.nr_of_rows());
    ExtremeRaysIndicator=ext;
    vector<bool> choice=ext;
    if (inhomogeneous) {
        // separate extreme rays to rays of the level 0 cone
        // and the verticies of the polyhedron, which are in level >=1
        size_t nr_gen = Generators.nr_of_rows();
        vector<bool> VOP(nr_gen);
        for (size_t i=0; i<nr_gen; i++) {
            if (ext[i] && v_scalar_product(Generators[i],Dehomogenization) != 0) {
                VOP[i] = true;
                choice[i]=false;
            }
        }
        VerticesOfPolyhedron=Generators.submatrix(VOP).sort_by_weights(WeightsGrad,GradAbs);
        is_Computed.set(ConeProperty::VerticesOfPolyhedron);
    }
    ExtremeRays=Generators.submatrix(choice);
    if(isComputed(ConeProperty::ModuleGeneratorsOverOriginalMonoid)){  // not possible in inhomogeneous case
        Matrix<Integer> ExteEmbedded=BasisChange.to_sublattice(ExtremeRays);
        for(size_t i=0;i<ExteEmbedded.nr_of_rows();++i)
            v_make_prime(ExteEmbedded[i]);
        ExteEmbedded.remove_duplicate_and_zero_rows();
        ExtremeRays=BasisChange.from_sublattice(ExteEmbedded);
    }
    ExtremeRays.sort_by_weights(WeightsGrad,GradAbs);
    is_Computed.set(ConeProperty::ExtremeRays);
}

//---------------------------------------------------------------------------

template<typename Integer>
void Cone<Integer>::set_zero_cone() {

    Generators = Matrix<Integer>(0,dim);
    is_Computed.set(ConeProperty::Generators);

    ExtremeRays = Matrix<Integer>(0,dim);
    is_Computed.set(ConeProperty::ExtremeRays);

    SupportHyperplanes = Matrix<Integer>(0,dim);
    is_Computed.set(ConeProperty::SupportHyperplanes);

    TriangulationSize = 0;
    is_Computed.set(ConeProperty::TriangulationSize);

    TriangulationDetSum = 0;
    is_Computed.set(ConeProperty::TriangulationDetSum);

    Triangulation.clear();
    is_Computed.set(ConeProperty::Triangulation);

    StanleyDec.clear();
    is_Computed.set(ConeProperty::StanleyDec);

    multiplicity = 1;
    is_Computed.set(ConeProperty::Multiplicity);

    HilbertBasis = Matrix<Integer>(0,dim);
    is_Computed.set(ConeProperty::HilbertBasis);

    Deg1Elements = Matrix<Integer>(0,dim);
    is_Computed.set(ConeProperty::Deg1Elements);

    HSeries = HilbertSeries(vector<num_t>(1,1),vector<denom_t>()); // 1/1
    is_Computed.set(ConeProperty::HilbertSeries);

    if (!is_Computed.test(ConeProperty::Grading)) {
        Grading = vector<Integer>(dim);
        GradingDenom = 1;
        is_Computed.set(ConeProperty::Grading);
    }

    pointed = true;

    deg1_extreme_rays = true;
    is_Computed.set(ConeProperty::IsDeg1ExtremeRays);

    deg1_hilbert_basis = true;
    is_Computed.set(ConeProperty::IsDeg1HilbertBasis);

    integrally_closed = true;
    is_Computed.set(ConeProperty::IsIntegrallyClosed);


    if (ExcludedFaces.nr_of_rows() != 0) {
        is_Computed.set(ConeProperty::ExcludedFaces);
        InExData.clear();
        InExData.push_back(make_pair(vector<key_t>(),-1));
        is_Computed.set(ConeProperty::InclusionExclusionData);
    }

    if (inhomogeneous) {  // empty set of solutions
        VerticesOfPolyhedron = Matrix<Integer>(0,dim);
        is_Computed.set(ConeProperty::VerticesOfPolyhedron);

        module_rank = 0;
        is_Computed.set(ConeProperty::ModuleRank);

        ModuleGenerators = Matrix<Integer>(0,dim);
        is_Computed.set(ConeProperty::ModuleGenerators);

        affine_dim = -1;
        is_Computed.set(ConeProperty::AffineDim);

        recession_rank = 0;
        is_Computed.set(ConeProperty::RecessionRank);
    }

    if (!inhomogeneous) {
        ClassGroup.resize(1,0);
        is_Computed.set(ConeProperty::ClassGroup);
    }

    if (inhomogeneous || ExcludedFaces.nr_of_rows() != 0) {
        multiplicity = 0;
        is_Computed.set(ConeProperty::Multiplicity);

        HSeries.reset(); // 0/1
        is_Computed.set(ConeProperty::HilbertSeries);

    }
}

} // end namespace libnormaliz
