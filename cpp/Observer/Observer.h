///////////////////////////////////////////////////////////
//  Observer.h
//  Implementation of the Class Observer
//  Created on:      07-十月-2014 23:00:10
//  Original author: cl
///////////////////////////////////////////////////////////

#if !defined(EA_2C7362B2_0B22_4168_8690_F9C7B76C343F__INCLUDED_)
#define EA_2C7362B2_0B22_4168_8690_F9C7B76C343F__INCLUDED_

class Subject;

class Observer
{

public:
	Observer();
	virtual ~Observer();
	virtual void update(Subject * sub) = 0;
};
#endif // !defined(EA_2C7362B2_0B22_4168_8690_F9C7B76C343F__INCLUDED_)
