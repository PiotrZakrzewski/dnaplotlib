#!/usr/bin/env python
"""
DNAplotlib SBOL Functionality
=============================
   This submodule extends the DNARenderer object to allow for rendering of SBOL
   objects generated by the pySBOL library. It also includes functions to navigate
   the object hierarchy.

   Be advised: this extention requires that pySBOL is fully installed and working.
"""
#    DNAplotlib
#    Copyright (C) 2015 by
#    Bryan Bartley <bartleyba@sbolstandard.org>
#    Thomas E. Gorochowski <tom@chofski.co.uk>
#    All rights reserved.
#    OSI Open Software License 3.0 (OSL-3.0) license.

import dnaplotlib as dpl

__author__ = "Bryan Bartley <bartleyba@sbolstandard.org>\n\
               Thomas E. Gorochowski <tom@chofski.co.uk>"
__license__ = "MIT"
__version__ = "1.0"


class SBOLRenderer(dpl.DNARenderer):

    def SO_terms(self):
        """Return dictionary of all standard built-in SBOL part renderers referenced by Sequence Ontology term"""
        return {
            "SO:0000167": "Promoter",
            "SO:0000316": "CDS",
            "SO:0000141": "Terminator",
            "SO:0000552": "RBS",
            "SO:0001953": "Scar",
            # No SO Term : 'Spacer',
            # No SO Term : 'EmptySpace',
            "SO:000037": "Ribozyme",
            "SO:0001977": "Ribonuclease",
            "SO:0001955": "ProteinStability",
            "SO:0001956": "Protease",
            "SO:0000057": "Operator",
            # SO term insulator does not have same semantics : 'Insulator',
            "SO:0000296": "Origin",
            "SO:0001932": "5Overhang",
            "SO:0001933": "3Overhang",
            "SO:0001687": "RestrictionSite",
            "SO:0000299": "RecombinaseSite",
            "SO:0001691": "BluntRestrictionSite",
            "SO:0005850": "PrimerBindingSite",
            "SO:0001694": "5StickyRestrictionSite",
            "SO:0001690": "3StickyRestrictionSite",
            "SO:0000001": "UserDefined",
            "SO:0001978": "Signature",
        }

    def renderSBOL(self, ax, target_component, part_renderers, opts=None, plot_backbone=True):
        """
        Render a design from an SBOL DNA Component

        Parameters
        ----------
        ax : matplotlib.axes
            Axes to draw the design to.

        target_component : sbol.DNAComponent
            An sbol.DNAComponent that contains the design to draw. The design must contain a series of subcomponents
            arranged in linear order

        part_renderers : dict(functions)
            Dict of functions where the key in the part type and the dictionary returns
            the function to be used to draw that part type.

        Returns
        -------
        start : float
            The x-point in the axis space that drawing begins.

        end : float
            The x-point in the axis space that drawing ends.
        """
        if not target_component.features:
            raise ValueError("DNAComponent does not have any features.  Cannot render SBOL.")
        dpl_design = (
            []
        )  # The SBOL data will be converted to a list of dictionaries used by DNAPlotLib
        for subcomponent in target_component.features:
            if not subcomponent.roles:
                raise ValueError("Subcomponent does not have a role.  Cannot render SBOL.")
            SO_term = subcomponent.roles[0].split("/")[-1]
            if SO_term in list(self.SO_terms().keys()):
                part = {}
                part["type"] = self.SO_terms()[SO_term]
                name = subcomponent.name
                if not name:
                    name = subcomponent.display_id
                part["name"] = name
                part["fwd"] = True
                if subcomponent.locations and len(subcomponent.locations) > 0:
                    part["start"] = subcomponent.locations[0].start
                    part["end"] = subcomponent.locations[0].end
                if opts:
                    part["opts"] = opts
                dpl_design.append(part)
        # sort the design by start position
        dpl_design = sorted(dpl_design, key=lambda k: k.get("start", 0))
        start, end = self.renderDNA(ax, dpl_design, part_renderers, plot_backbone=plot_backbone)
        return start, end
