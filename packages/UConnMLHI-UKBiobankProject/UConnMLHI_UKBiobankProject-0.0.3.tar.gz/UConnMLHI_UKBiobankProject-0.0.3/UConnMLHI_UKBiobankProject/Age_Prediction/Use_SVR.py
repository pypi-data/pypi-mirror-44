__auther__ = 'Xinyu Wang'

def run_CrossValidation(X,y,cv=5,random_state=0,return_format='np'):
    # Build lasso and fit
    lasso = LassoCV(cv=cv, random_state=0)
    lasso.fit(X, y)


    # Read out attributes
    coeffs = lasso.coef_         # dense np.array
    # coeffs = lasso.sparse_coef_  # sparse matrix

    # coeffs = lasso.intercept_    # probably also relevant
    if return_format == 'np':
        return coeffs
    else:
        # TODO
        return coeffs
